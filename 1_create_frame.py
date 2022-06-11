from encodings import utf_8
import pygame

# �젆�뜄占쏙옙 筌띾슡占쏙옙疫뀐옙

pygame.init()
# �룯�뜃由곤옙�넅. pygame import占쎈뻻 獄쏆꼶諭띰옙�뻻 占쎌깈�빊�뮉鍮먧빳占쏙옙�뼄.

# 占쎌넅筌롳옙 占쎄쾿疫뀐옙 占쎄퐬占쎌젟
screen_width = 480  # 揶쏉옙嚥∽옙 占쎄쾿疫뀐옙
screen_height = 640  # 占쎄쉭嚥∽옙 占쎄쾿疫뀐옙
screen = pygame.display.set_mode((screen_width, screen_height))

# 占쎌넅筌롳옙 占쏙옙占쏙옙�뵠占쏙옙占� 占쎄퐬占쎌젟
pygame.display.set_caption("Nado Game")

# 占쎈늄嚥≪뮄�젃占쎌삪 �넫�굝利븝옙由븝쭪占� 占쎈륫占쎈즲嚥∽옙 占쏙옙占썸묾占�
# 占쎌뵠甕겹끋�뱜 �뙴�뫂遊�
running = True  # 野껊슣�뿫占쎌뵠 筌욊쑵六얌빳臾믪뵥筌욑옙 占쎌넇占쎌뵥占쎈릭占쎈뮉 癰귨옙占쎈땾
while running:
    for event in pygame.event.get():  # 占쎈선占쎈샥 占쎌뵠甕겹끋�뱜揶쏉옙 獄쏆뮇源� 占쎈릭占쏙옙占쏙옙�뮉揶쏉옙?
        if event.type == pygame.QUIT:  # 筌≪럩�뵠 占쎈뼍占쎌뿳占쎈뮉 占쎌뵠甕겹끋�뱜揶쏉옙 獄쏆뮇源� 占쎈릭占쏙옙占쏙옙�뮉揶쏉옙?
            running = False  # 野껊슣�뿫占쎌뵠 筌욊쑵六얌빳臾믪뵠 占쎈툡占쎈빍野껊슢留�

# pygame �넫�굝利�
pygame.quit()
