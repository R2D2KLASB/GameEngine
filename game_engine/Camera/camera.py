import time
import cv2
import numpy as np


class ShipDetection:
    def __init__(self, queue=False, publisher=False):
        self.queue = queue
        self.publisher = publisher

    def select_frame(self):
        cv2.namedWindow("preview")
        #Select Source
        vc = cv2.VideoCapture(2)
        frame_height = 0
        frame_width = 0
        vc.set(3, 1920)
        vc.set(4, 1080)

        if vc.isOpened(): # try to get the first frame
            rval, frame = vc.read()
        else:
            rval = False
        result = False
        if self.publisher:
            self.publisher['intern'].send('getPos')
        while rval:
            rval, frame = vc.read()
            cv2.imshow("preview", frame)
            if self.publisher:
                result = self.queue.read(wait=False)
            key = cv2.waitKey(20)
            if key == 32 or result: # exit on SPACEBAR
                if self.publisher:
                    self.publisher['intern'].send('ok')
                    result = self.queue.read(wait=True)
                    print(result)
                cv2.destroyAllWindows()
                return frame

    def get_perspective(self, img, location, height = 804, width = 804):
        loc_index = list(range(4))

        x = 0
        y = 1

        top_left = 0
        top_right = 0                       
        bot_left = 0
        bot_right = 0
        
        max_sum = location[0][0][x] + location[0][0][y]
        min_sum = location[0][0][x] + location[0][0][y]
        
        # find top left and bottom right
        for i in loc_index:
            if location[i][0][x] + location[i][0][y] >= max_sum:
                max_sum = location[i][0][x] + location[i][0][y]
                bot_right = i
            if location[i][0][x] + location[i][0][y] <= min_sum:
                min_sum = location[i][0][x] + location[i][0][y]
                top_left = i
        
        # pop index of found loc_index
        if top_left > bot_right:
            loc_index.pop(top_left)
            loc_index.pop(bot_right)
        else:
            loc_index.pop(bot_right)
            loc_index.pop(top_left)

        # find top right and bottom left with the two leftover loc_index
        if location[loc_index[0]][0][y] >= location[loc_index[1]][0][y]:
            bot_left = loc_index[0]
            top_right = loc_index[1]
        else:
            bot_left = loc_index[1]
            top_right = loc_index[0]


        pts1 = np.float32([location[top_left], location[top_right], location[bot_left], location[bot_right]])
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

        # Apply Perspective Transform Algorithm
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(img, matrix, (width, height))
        return result

    def detect_board(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        bilateral_filtered = cv2.bilateralFilter(gray_image, 13, 20, 20)
        canny_filtered = cv2.Canny(bilateral_filtered, 30, 180)

        contours, hierarchy = cv2.findContours(canny_filtered.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour_image = cv2.drawContours(image = image.copy(), contours = contours, contourIdx = -1, color = (0, 255, 0), thickness = 1)

        # cv2.imshow('board', contour_image)
        # cv2.waitKey()
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]
        location = None

        # Finds rectangular contour
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 15, True)
            if len(approx) == 4:
                location = approx
                break
        result = self.get_perspective(image, location)
        # Resultaat showen in interface zodat zeker is dat veld goed gedetecteerd is
        # cv2.imshow('board', result)
        # cv2.waitKey()
        return result, location

    def split_boxes(self, board):
        """Takes an image of the board and split it into 100 cells (10 x 10).
        each cell contains an element of that board is either occupied or an empty cell."""
        rows = np.vsplit(board, 12)
        del rows[-1]
        del rows[0]
        boxes = []
        for row in rows:
            cols = np.hsplit(row,12)
            del cols[-1]
            del cols[0]
            for box in cols:
                boxes.append(box)
                # cv2.imshow('board', box)
                # cv2.waitKey()
        return boxes

    def create_2D_field(self, boxes):
        field = np.arange(100)
        field = field.reshape((10, 10))
        field = np.zeros_like(field)
        index = 0

        for box in boxes:
            total_pixels = len(box) * len(box[0])
            pixels_filled = 0
            blur = cv2.GaussianBlur(box,(5,5),0)
            for y in range(len(box)):
                for x in range(len(box[y])):
                    if box[y][x] >= 70:
                        box[y][x] = 255
                    else:
                        box[y][x] = 0
                        pixels_filled += 1
            pixel_ratio = ((pixels_filled / total_pixels) * 100)
            if pixel_ratio > 80:
                field[index // 10][index % 10] = 1
            index += 1
        # print board with 0 for empty cells and 1 for boats
        # print(field)
        return field

    def get_boats(self, field):
        coorinates_checked = []
        boats = []
        for y in range(len(field)):
            for x in range(len(field[y])):
                length = 1
                if field[y][x] == 1:
                    if ([y, x] in coorinates_checked):
                        pass
                    else:
                        boat = []
                        coorinates_checked.append([y, x])
                        boat.append([y, x])
                        if ((y+length) < 10) and field[y + length][x] == 1:
                            while field[y + length][x] == 1:
                                coorinates_checked.append([y + length, x])
                                boat.append([y + length, x])
                                if (y + length) < 9:
                                    length += 1
                                else:                                                                                                                                                                                                                                                                                                                                          
                                    break
                        elif ((x + length) < 10) and field[y][x + length] == 1:
                            while field[y][x + length] == 1:
                                coorinates_checked.append([y, x + length])
                                boat.append([y, x + length])
                                if (x + length) < 9:
                                    length += 1
                                else:
                                    break
                        boats.append(boat)
        # print boat list
        # for boat in boats:
        #     print(boat)
        return boats

    def detect_and_return_boats(self, image):
        # use this to make frame with webcam
        # frame = select_frame()
        # board, location = detect_board(frame)

        # use this for premade frame
        board, location = self.detect_board(image)

        gray_image = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
        boxes = self.split_boxes(gray_image)
        field = self.create_2D_field(boxes)
        boat_list = self.get_boats(field)

        return boat_list

    def webcam_detection(self):
        # use this to make frame with webcam
        frame = self.select_frame()
        board, location = self.detect_board(frame)

        # use this for premade frame
        # board, location = detect_board(image)

        gray_image = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
        boxes = self.split_boxes(gray_image)
        field = self.create_2D_field(boxes)
        boat_list = self.get_boats(field)

        return boat_list

    # boat_list = webcam_detection()
    # for boat in boat_list:
    #     print(boat)