from . import base, player

cloud1_list = []
cloud0_list = []
cloud0_disappear_time = [2]


class Cloud(base.Base):
    def __init__(self, cloud_type, x, y, picture_num, disappear_picture_list):
        base.Base.__init__(self, x, y)
        self.cloud_type = cloud_type
        self.hitted = False
        self.touched = False
        self.disappear_picture_list = disappear_picture_list
        self.disappear_picture_num = picture_num
        self.picture_count = 0
        self.image_index = 0

    def display(self, screen):
        global hit_score
        global cloud_disappear_time
        screen.blit(self.disappear_picture_list[0], (self.x, self.y))
        # if self.hitted == True and self.image_index < self.disappear_picture_num:
        #     screen.blit(self.disappear_picture_list[self.image_index], (self.x, self.y))
        #     self.picture_count += 1
        #     if self.picture_count == cloud_disappear_time[self.cloud_type]:
        #         self.picture_count = 0
        #         self.image_index += 1
        # elif self.image_index < self.disappear_picture_num:
        #     screen.blit(self.disappear_picture_list[0], (self.x, self.y))
        # if self.hitted == True and self.image_index >= self.disappear_picture_num:
        #     del_cloud(self)
        if self.y > 900 or self.x < -100:
            del_cloud(self)

    # def isHitted(self, width, height, player_rect):
    #     self.touched = False
    #     if player_rect.x < self.x + width and player_rect.x + 26 > self.x:
    #         if player_rect.y - height < self.y < player_rect.y + 45:
    #             self.hitted = True
    #             self.touched = True

    # stand时， 碰到云，hitted为True，但touched为False


def del_cloud(cloud):
    global cloud0_list
    if cloud in cloud0_list or cloud1_list:
        cloud0_list.remove(cloud)


def clear_cloud():
    cloud1_list.clear()
    cloud0_list.clear()