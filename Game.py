import numpy as np
import random
import cv2
import time

class Snake:
    def __init__(self):
        self.img = np.zeros((500,500,3), dtype='uint8')
        self.snake_position = [[250,250], [240,250], [230,250]]
        self.apple_position = [random.randrange(1,50)*10, random.randrange(1,50)*10]
        self.score = 0
        self.prev_button_direction = 1
        self.button_direction = 1
        self.snake_head = [250,250]
        self.k = -1
        #self.game_over = False

    def __str__(self):
        return f"SnakeGame with score {self.score}"

    def isCollisionWithApple(self):
        self.apple_position = [random.randrange(1,50)*10,random.randrange(1,50)*10]
        self.score += 1

    def isCollisionWithBoundaries(self):
        if self.snake_head[0]>=500 or self.snake_head[0]<0 or self.snake_head[1]>=500 or self.snake_head[1]<0 :
            return 1
        else:
            return 0

    def isCollisionWithSelf(self):
        snake_head = self.snake_position[0]
        if snake_head in self.snake_position[1:]:
            return 1
        else:
            return 0

    def imgStart(self):
        cv2.imshow('Snake OpenCV Game', self.img)
        cv2.waitKey(1)
        self.img = np.zeros((500,500,3),dtype='uint8')
        # Display Apple
        cv2.rectangle(self.img,(self.apple_position[0],self.apple_position[1]),(self.apple_position[0]+10,self.apple_position[1]+10),(0,0,255),3)
        # Display Snake
        for position in self.snake_position:
            cv2.rectangle(self.img,(position[0],position[1]),(position[0]+10,position[1]+10),(0,255,0),3)

    def listenerKey(self):
        # Takes step after fixed time
        t_end = time.time() + 0.2
        self.k = -1
        while time.time() < t_end:
            if self.k == -1:
                self.k = cv2.waitKey(125)
            else:
                continue

    def parseKey(self):
        # 0-Left, 1-Right, 3-Up, 2-Down, q-Break
        # a-Left, d-Right, w-Up, s-Down

        if self.k == ord('a') and self.prev_button_direction != 1:
            self.button_direction = 0
        elif self.k == ord('d') and self.prev_button_direction != 0:
            self.button_direction = 1
        elif self.k == ord('w') and self.prev_button_direction != 2:
            self.button_direction = 3
        elif self.k == ord('s') and self.prev_button_direction != 3:
            self.button_direction = 2
        elif self.k == ord('q'):
            self.button_direction - 1
        else:
            self.button_direction = self.button_direction

    def updateHeadPosition(self):
        # Change the head position based on the button direction
        if self.button_direction == 1:
            self.snake_head[0] += 10
        elif self.button_direction == 0:
            self.snake_head[0] -= 10
        elif self.button_direction == 2:
            self.snake_head[1] += 10
        elif self.button_direction == 3:
            self.snake_head[1] -= 10

    def eatApple(self):
        # Increase Snake length on eating apple
        if self.snake_head == self.apple_position:
            self.isCollisionWithApple()
            self.snake_position.insert(0,list(self.snake_head))
        else:
            self.snake_position.insert(0,list(self.snake_head))
            self.snake_position.pop()

    def imgEnd(self):
        font = cv2.FONT_HERSHEY_SIMPLEX
        self.img = np.zeros((500,500,3),dtype='uint8')
        cv2.putText(self.img,'Your Score is {}'.format(self.score),(140,250), font, 1,(255,255,255),2,cv2.LINE_AA)
        cv2.imshow('Snake OpenCV Game', self.img)
        cv2.waitKey(0)
        cv2.imwrite('score.jpg',self.img)

    def isGameOver(self):
        # On collision kill the snake and print the score
        return self.isCollisionWithBoundaries() == 1 or self.isCollisionWithSelf() == 1

    def run(self):
        while True:
            self.imgStart()
            self.listenerKey()
            self.parseKey()

            # Quit
            if self.button_direction == -1:
                break

            self.prev_button_direction = self.button_direction
            self.updateHeadPosition()
            self.eatApple()

            if self.isGameOver():
                self.imgEnd()
                break

        cv2.destroyAllWindows()
