---
title: 開発サーバーでもテストでも、MSWでAPIモックを利用する
tags:
  - フロントエンド
  - React
  - vite
  - msw
  - Vitest
private: false
updated_at: '2025-12-09T00:42:47+09:00'
id: d1175d9d2cfd1ed92e60
organization_url_name: null
slide: false
ignorePublish: false
posting_campaign_uuid: null
agreed_posting_campaign_term: false
---
## この記事は何？
- ReactプロジェクトにMSWを導入して、バックエンドの開発が進んでいないプロジェクトでも、まるでAPIサーバーがあるかのように実行できる環境を作る
- VitestでAPIのモックを作成をしなくても動くようにする

## MSW導入の動機
バックエンド(APIサーバー)の開発や通信の設定が済んでいないタイミングでフロントエンドのvite開発サーバーを起動したとき、APIのエンドポイントが無いために表示がエラーになり、開発がうまく進んでいかないというシチュエーションがありました。

こんな時、開発サーバーからのAPIリクエストを受け取ってくれるAPIサーバーがあると非常に便利です。
このような仕組みとして、json-serverのようなものもありますが、明示的に起動をする必要があるのが少し面倒です。devcontainerであればdocker-composeを作成することで手間は省けますが、常にコンテナが起動していてリソースの心配がある、dockerNWの設定に気を使う必要があるなどの理由でしっくり来ていませんでした。

今回導入するMSWはそんな問題を一気に解決してくれるAPIモックのソリューションです。
viteの開発サーバーを起動すると同時にモックサーバーも立ち上がる、レスポンスの出し分けのロジックを書くことができるなど、機能は十分に充実しています。


## MSWの導入
以下でインストールを実行し、依存関係に追加します。
```bash
yarn add -D msw
```

## 開発サーバーで動くようにする
### 1. 環境設定
以下のコマンドを実行して、モックの起動を有効にします。
```bash
npx msw init public/ --save
```
`public/mockServiceWorker.js` が自動生成されるほか、`packages.json` への設定も追加されます。

:::note info
`public/`以外のディレクトリに配置することも技術的にはできるようですが、各所に設定を追加する必要があるようです。
このような特殊な設定内容は往々にして忘れてしまうので、後に見返した時の負債になりかねないと思い、今回は実施しませんでした。
:::

### 2. サーバー設定
:::note info
以下では `src/mocks/` 以下にMSW関連のファイルを配置していきます
:::
以下のファイルを作成する。
```typescript:src/mocks/browser.ts
import { setupWorker } from 'msw/browser';
import { handlers } from './handlers.ts';

export const worker = setupWorker(...handlers);
```

```typescript:handlers.ts
import { userHandlers } from './handlers/user';

export const handlers = [
  ...userHandlers,
  // 将来的にエンドポイントが増えたら、スプレッド構文で追加していく
  // ...postHandlers,
  // ...authHandlers,
];
```

以下はMSWのAPIサーバーとしての具体的な設定内容になるので、参考程度にご覧ください。
```typescript:src/mocks/handlers/user.ts
import { http, HttpResponse } from 'msw';
import type { User } from '@/shared/types/User';

type Sort = 'id' | 'post_count';
type Order = 'asc' | 'desc';

// モック用テストデータ
export const mockUsers: User[] = [
  {
    id: '1',
    name: 'nobunaga oda',
    post_count: 3
  },
  {
    id: '2',
    name: 'mitsuhide akechi',
    post_count: 100
  },
];

export const userHandlers = [
  http.get('*/users', ({ request }) => {
    const url: URL = new URL(request.url);
    const sort: Sort | null = url.searchParams.get('sort') as Sort;
    const order: Order | null = url.searchParams.get('order') as Order;
    const limit: number | null = parseInt(
      url.searchParams.get('limit') as string,
    );

    let users = [...mockUsers];

    // ソート処理
    if (sort && order) {
      switch (sort) {
        case 'id':
          users.sort((a, b) =>
            order === 'desc'
              ? parseInt(b.id) - parseInt(a.id)
              : parseInt(a.id) - parseInt(b.id),
          );
          break;
        case 'post_count':
          users.sort((a, b) =>
            order === 'desc' ? b.post_count - a.post_count : a.post_count - b.post_count,
          );
          break;
      }
    }

    // リミット処理
    if (limit) {
      users = users.slice(0, limit);
    }

    return HttpResponse.json({ users });
  }),
];
```


### 3. 実際に呼び出してみる
`main.tsx` で、開発環境実行時にMSWを呼ぶように設定します。
```diff_tsx:src/main.tsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@/main.css';
import Home from '@/pages/home/home.tsx';

+ async function enableMocking() {
+   if (!import.meta.env.DEV) {
+     return;
+   }
+ 
+   const { worker } = await import('@/mocks/browser');
+   await worker.start({ onUnhandledRequest: 'bypass' }); //外部APIはモックせず普通に叩く
+ }
+ 
+ enableMocking().then(() => {
  createRoot(document.getElementById('root')!).render(
    <StrictMode>
      <Home />
    </StrictMode>,
  );
+ });
```

以下のようなapi定義を作成してコンポーネントで `getUsers()` を呼び出すことでjsonレスポンスを受け取ることができます。
```typescript:src/feature/user/api/getUsers.ts
export const getUsers = async () => {
  const response = await axios.get<userResponse>(
    '/users?sort=post_count&order=desc',
  );
  console.debug('API Response:', response.data);
  return response.data.users;
};
```


## テストでMSWを使えるようにする
### 1. コンフィグ設定
`vitest.config.ts` に以下のような設定を追加して、すべてのテストでMSWが設定されている状態になるようにします。
```typescript:vitest.config.ts
import '@testing-library/jest-dom/vitest';
import { beforeAll, afterAll, afterEach } from 'vitest';

import { server } from './src/mocks/server';

// テスト開始時にMSWサーバーを起動
beforeAll(() => {
  server.listen({ onUnhandledRequest: 'error' }); // 未定義のエンドポイント呼び出しを発見したら即error
});

// 各テスト後にMSWハンドラーをリセット
afterEach(() => {
  server.resetHandlers();
});

// テスト終了時にMSWサーバーを停止
afterAll(() => {
  server.close();
});
```

### 2. サーバー設定
開発サーバーの設定で追加した `handlers.ts` に加え、以下を作成します。
```typescript:src/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers.ts';

export const server = setupServer(...handlers);
```

:::note info
ここでは開発サーバー用の設定で使ったものと同じハンドラーを使うようにしています。
テスト用の独自のAPIエンドポイントを利用したい場合などには、この `server.ts` で呼び出すhandlersを `browser.ts` と共通化せず、独自に追加してください。
:::

### 3. テストから呼び出してみる
特に記載をする必要はありません。テスト実行時にMSWサーバーも自動的に立ち上がり、APIリクエストはMSWに自動的に流れます。

:::note info
自論ですが、APIの正常系UTではMSWモックを利用する価値はあまりないと考えています。APIのUTでは、「仕様通りのエンドポイントにリクエストを飛ばしていること」などを確認するべきで、どのようなデータが返ってきているかはAPIサーバー側のAPIテストの責任ではないかと思います。

このような場合にはMSWは利用せず、UTファイル内で `vi.mocked(axios.get)` などを使ってリクエストそのものをモック化し、`axios.get` が呼び出されたか？どこにリクエストしたか？を確認するようにしてください。

なお、MSWを使わないようにする場合には、個別に何か記載をする必要はありません。`vi.mocked()` はnode環境内で完結する動きであり、NWレイヤーで動くMSWに到達する前に処理されるからです。
:::


## 最後に
実は今回、趣味としては初めて本腰を入れてフロントエンド開発を始めてみました。開発環境・開発体験の改善に興味があり、MSWにたどり着きました。
json-serverは知っていましたが、本文中でも述べた通り開発環境の作り方にやや不満があり採用しませんでした。
MSWはNWレイヤーで動くためAPレイヤーでの特別な設定が不要で、しかも本来は存在しないはずのエンドポイントへのリクエストを横取りして処理してくれるので、APIサーバーに関して特別考えることなく開発を進めることができ、今のところ非常に体験が良いです。

若干話は逸れますが、突き詰めるとviteの開発サーバーのホットリロードに頼りきりではなく、storybookなどの導入を進めるべきなのかなとも思っています。
storybookとMSWの連携方法についても、機会があればまとめたいと思います。



## 参考資料
1. [【MSW公式】Quick start](https://mswjs.io/docs/quick-start)
2. [Vitest で API 通信のモックはどうしてる？主要3パターン（vi.mock / MSW / Queryキャッシュ）を比較・使い分け](https://zenn.dev/apple_yagi/articles/0544ef8258b6d7)

## special thanks
1. Gemini 3.0 Pro
2. GPT-5.1-Codex
