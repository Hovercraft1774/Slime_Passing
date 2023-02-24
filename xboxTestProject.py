import pygame as pg

BLACK = pg.Color("black")
WHITE = pg.Color("white")





class TextPrint(object):
    def __init__(self,fontsize):
        self.fontsize = fontsize
        self.x = ""
        self.y = ""
        self.line_height = ""
        self.font = pg.font.Font(None, self.fontsize)
        self.reset()

    def tprint(self,screen,text):
        textBitmap = self.font.render(text,True,BLACK)
        screen.blit(textBitmap,(self.x,self.y))
        self.y += self.line_height



    def reset(self):
        self.x = 15
        self.y = 15
        self.line_height = self.fontsize - 5

    def indent(self):
        self.x += 10
    def unindent(self):
        self.x -= 10


pg.init()
screen = pg.display.set_mode((500,800))
pg.display.set_caption("Xbox Testing Controller")

running = True

clock = pg.time.Clock()
fps = 40
text = TextPrint(25)
pg.joystick.init()

controller_list = []







while running:


    #tick clock
    clock.tick(fps)

    #get inputs
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.JOYBUTTONDOWN: #pressing button
            print("Pressed a button")
        if event.type == pg.JOYBUTTONUP: #releasing button
            print("Released a button")
    screen.fill(WHITE)
    text.reset()

    joystick_count = pg.joystick.get_count() #number of joysticks
    text.tprint(screen,"number of joysticks {}".format(joystick_count))
    text.indent()

    for i in range(joystick_count):
        controller = pg.joystick.Joystick(i)
        controller.init()
        controller_list.append(controller)

        try:
            cont_id = controller.get_instance_id()
        except AttributeError:
            cont_id = controller.get_id()
        text.tprint(screen,"Controller {}".format(cont_id))
        text.indent()

        cont_name = controller.get_name()
        text.tprint(screen, "controller name {}".format(cont_name))

        try:
            guid = controller.get_guid()
        except AttributeError:
            pass
        else:
            text.tprint(screen,"GUID {}".format(guid))

        axes = controller.get_numaxes() #number of stuff
        text.tprint(screen, "Number of axes {}".format(axes))
        text.indent()
        for i in range(axes): # joysticks, triggers and their values
            axis = controller.get_axis(i)
            text.tprint(screen, "Axis {0} value {1:6.3f}".format(i,axis))
        text.unindent()

        buttons = controller.get_numbuttons()
        text.tprint(screen, "Number of buttons: {}".format(buttons))
        text.indent()

        for i in range(buttons): #a,b,y, etc
            button = controller.get_button(i)
            text.tprint(screen,"Button {:>2} value: {}".format(i, button))
        text.unindent()

        hats = controller.get_numhats()
        text.tprint(screen, "Number of hats: {}".format(hats))
        text.indent()

        for i in range(hats): #d-pad
            hat = controller.get_hat(i)
            text.tprint(screen, "Hat {} value: {}".format(i,hat))
        text.unindent()
        text.unindent()



    #update

    #draw

    pg.display.flip()

pg.quit()
quit()



