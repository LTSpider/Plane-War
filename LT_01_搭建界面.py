import pygame  # 导入动态模块(.dll .pyd .so) 不需要在包名后边跟模块名

# 定义常量(定义后,不再改值)
WINDOW_HEIGHT = 768
WINDOW_WIDTH = 512


def main():
    """主函数  一般将程序的入口"""
    pygame.init()
    # 创建窗口  set_mode((窗口尺寸))
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # 将图片加载到内存中  load(图片资源路径)
    bg_img = pygame.image.load("res/img_bg_level_1.jpg")

    while True:
        # 贴图 把图片贴到窗口中  blit(图片对象, 相对原点的坐标)
        window.blit(bg_img, (0, 0))
        # 刷新界面  不刷新不会更新显示的内容
        pygame.display.update()

if __name__ == '__main__':  # 判断是否主动执行该文件
    main()