from time import sleep
import time
from reprint import output
from math import floor
import click
import vlc


class Scenery:
    def __init__(self, Cow, Grass):
        self.grass = Grass
        self.cow = Cow

    def _get_draw_lines(self):
        return len(self.draw().split('\n'))

    def draw(self):
        return str(self.cow.draw()) + str(self.grass)

    def timer(self, refresh_interval=0.5, minutes=None):
        with output(  # use reprint output to reprint multi-line in the console
            initial_len=self._get_draw_lines(),
            interval=0
        ) as output_lines:
            t_start = time.time()
            if minutes:  # if minutes is specified, show timer
                t_end = time.time() + 60 * minutes
                while time.time() < t_end:
                    elapsed_time = time.time() - t_start
                    remaining_time = round(minutes - elapsed_time / 60, 2)
                    remaining_time_formatted = f'{int(remaining_time)}:{int(remaining_time % 1 * 60):02}'
                    self.cow.say(f"Ending walk in {remaining_time_formatted} minutes")
                    to_draw = self.draw()
                    to_draw_line_by_line = to_draw.split('\n')
                    for i in range(len(to_draw_line_by_line)):
                        output_lines[i] = to_draw_line_by_line[i]
                    sleep(refresh_interval)
            else:  # if minutes is not specified, show elapsed time
                while True:
                    elapsed_time = time.time() - t_start
                    elapsed_time_formatted = f'{int(elapsed_time / 60)}:{int(elapsed_time):02}'
                    self.cow.say(f"Walked for {elapsed_time_formatted} minutes")
                    to_draw = self.draw()
                    to_draw_line_by_line = to_draw.split('\n')
                    for i in range(len(to_draw_line_by_line)):
                        output_lines[i] = to_draw_line_by_line[i]
                    sleep(refresh_interval)


class TextBubble:
    def __init__(self, text):
        self.text = text
        self.width = len(self.text) + 4  # 4 is the spacing for the frame
        self.bubble = '_' * self.width + '\n< ' + self.text + ' >\n' + '-' * self.width


class Grass:
    def __init__(self):
        self.grass = '^' * 40

    def __repr__(self):
        return self.grass


class CowLegs:
    def __init__(self):
        self.is_walking = False
        self.legs = self.standing()

    def update(self, cow_is_walking):
        self.is_walking = cow_is_walking
        if self.is_walking:
            self.legs = self.walking()
        else:
            self.legs = self.standing()

    def standing(self):
        return '||     ||'

    def walking(self):
        legs_move_forward_1 = '|\\     |\\'
        legs_move_forward_2 = '/|     /|'

        if self.legs == self.standing():
            return legs_move_forward_1
        elif self.legs == legs_move_forward_1:
            return legs_move_forward_2
        elif self.legs == legs_move_forward_2:
            return legs_move_forward_1


class CowTail:
    def __init__(self):
        self.is_walking = False
        self.tail = self.stationary()

    def update(self, cow_is_walking):
        self.is_walking = cow_is_walking
        if self.is_walking:
            self.tail = self.wiggle()
        else:
            self.tail = self.stationary()

    def stationary(self):
        return '/\\/'

    def wiggle(self):
        tail_move_forward = '\\/\\'
        if self.tail == self.stationary():
            return tail_move_forward
        else:
            return self.stationary()


class CowEyes:
    def __init__(self):
        self.is_walking = False
        self.eyes = self.open()
        self.blink_interval = 3  # blink every 3 seconds
        self.previous_blink_time = time.time()

    def update(self, cow_is_walking):
        self.is_walking = cow_is_walking
        if self.is_walking and time.time() >= self.previous_blink_time + self.blink_interval:
            self.eyes = self.blink()
            self.previous_blink_time = time.time()
        else:
            self.eyes = self.open()

    def open(self):
        return 'oo'

    def blink(self):
        blink = '..'
        if self.eyes == self.open():
            return blink
        else:
            return self.open()


class Cow:
    """
    General pattern: self.draw() calls self.update().

    Additional functions can be written to update the state of the entity.
    These functions should be called in the self.update() method to update
    individual properties of the entity.

    Follows the Composition pattern where parts of the cow that should be
    animated are injected into the Cow class.

    """

    def __init__(self, CowLegs, CowTail, CowEyes):
        self.cow_legs = CowLegs
        self.cow_tail = CowTail
        self.cow_eyes = CowEyes
        self.greet = 'Moo!'
        self.text_bubble = TextBubble(self.greet)
        self.is_walking = False
        self.cow = self.draw()

    def __repr__(self):
        return self.cow

    def draw(self):
        return self.update()

    def _padded_text_bubble(self, midpoint):
        text_bubble_line_by_line = self.text_bubble.bubble.split('\n')
        new_text_bubble_list = []
        for line in text_bubble_line_by_line:
            # 20 is a magic number. Change to see the effects
            # the attempt to align the text bubble at the center
            # will fail when the text is too long
            new_text_bubble_list.append(' ' * (20-midpoint) + line)
        return '\n'.join(new_text_bubble_list)

    def update(self):
        self.cow_legs.update(self.is_walking)
        self.cow_tail.update(self.is_walking)
        self.cow_eyes.update(self.is_walking)
        text_bubble_midpoint = floor(len(self.text_bubble.bubble.split('\n')[-1])/2)
        return f'''
{self._padded_text_bubble(text_bubble_midpoint)}
            ^__^   /
    _______/({self.cow_eyes.eyes})  /
{self.cow_tail.tail}(       /(__)
    ||w----||
    {self.cow_legs.legs}
'''

    def walk(self):
        self.is_walking = True

    def stay(self):
        self.is_walking = False

    def say(self, text=None):
        if text:
            self.text_bubble = TextBubble(text)
        else:
            self.text_bubble = TextBubble(self.greet)


@click.command()
@click.option('--m', '--minutes', 'minutes', default=None, type=int, help='Number of minutes that the cow walks.')
def main(minutes):
    cow_legs = CowLegs()
    cow_tail = CowTail()
    cow_eyes = CowEyes()
    cow = Cow(cow_legs, cow_tail, cow_eyes)
    grass = Grass()
    cow.walk()
    scenery = Scenery(cow, grass)

    scenery.timer(minutes=minutes)

    # play moo sound after the walk timer ends
    p = vlc.MediaPlayer('moo.mp3')
    p.play()
    time.sleep(5)  # allow sufficient time to play the sound before the program terminates


if __name__ == "__main__":
    main()
