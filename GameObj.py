MIDDLE = 1
CORNER = 2 

class GameObj:
    def __init__(self, left=0, right=0, top=0, bottom=0):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
    
    def test_collision(self, other):
        if self.top >= other.bottom and self.bottom <= other.top:
            if self.right >= other.left and self.left <= other.right:
                other_size = other.right - other.left
                dif = other.right - self.right 
                if (abs(dif) > other_size * 0.3) and  (abs(dif) < other_size * 0.6):
                    return [True, MIDDLE]
                return [True, CORNER]
            else:
                return [False]    
        else: 
            return [False]