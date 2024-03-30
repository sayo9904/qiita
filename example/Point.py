import math

class Point:
    """
    平面上の点を表現するクラス
    """
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        
        self.r = math.sqrt(x**2 + y**2) # 原点からの距離 r は x, yの2乗和のルート
        self.theta = math.atan(y/x) # 点を原点からの平面ベクトルとしたときのx軸からの角度
        
        self.vx = 0
        self.vy = 0
    
    def print_coordinates(self) -> None:
        print(f'x = {self.x}')
        print(f'y = {self.y}')
        print(f'r = {self.r}')
    
    
    def get_velocity(self) -> float:
        """
        点の平面上の速度を返すメソッド
        """
        return math.sqrt(self.vx**2 + self.vy**2)
    
    
if __name__ == '__main__':
    a = "hoge"
    # print('activated main part of "Point.py"')
    myPoint = Point(2, 2)
