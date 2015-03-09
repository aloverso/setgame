"""lmr - planes.gui widgets with left-mid-right backgrounds.

   Copyright 2012, 2013 by Florian Berger <fberger@florian-berger.de>

   Module doctests:

   >>> display = planes.Display((300, 300))
   >>> display.image.fill((128, 128, 128))
   <rect(0, 0, 300, 300)>
   >>> def exit(plane):
   ...     pygame.quit()
   ...     raise SystemExit
   >>> button_1 = LMRButton("Default", 100, exit)
   >>> button_1.rect.center = (150, 30)
   >>> display.sub(button_1)
   >>> button_2 = LMRButton("BLACK", 100, exit, BLACK_BUTTON_STYLE)
   >>> button_2.rect.center = (150, 70)
   >>> display.sub(button_2)
   >>> button_3 = LMRButton("WHITE", 100, exit, WHITE_BUTTON_STYLE)
   >>> button_3.rect.center = (150, 110)
   >>> display.sub(button_3)
   >>> button_4 = LMRButton("ORANGE", 100, exit, ORANGE_BUTTON_STYLE)
   >>> button_4.rect.center = (150, 150)
   >>> display.sub(button_4)
   >>> option_list = LMROptionList("option_list",
   ...                             ["Option 1", "Option 2", "Option 3"],
   ...                             250)
   >>> option_list.rect.center = (150, 230)
   >>> display.sub(option_list)
   >>> clock = pygame.time.Clock()
   >>> while True:
   ...     events = pygame.event.get()
   ...     display.process(events)
   ...     display.update()
   ...     display.render()
   ...     pygame.display.flip()
   ...     clock.tick(30)
   Traceback (most recent call last):
       ...
   SystemExit
"""

# This file is part of planes.
#
# planes is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# planes is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with planes.  If not, see <http://www.gnu.org/licenses/>.

# work started on 27. Feb 2012

import planes.gui
import pygame
import os.path

class LMRStyle:
    """This class encapsulates the left, mid and right images to be used as widget background, as well as the text color.

       Attributes:

       LMRStyle.left_img
           A Pygame Surface, holding the left edge of the background image.

       LMRStyle.mid_img
           A Pygame Surface, holding the middle part of the background image.
           A widget might repeat this image to fit the desired width.

       LMRStyle.right_img
           A Pygame Surface, holding the right edge of the background image.

       LMRStyle.text_color
           An (R, G, B) color tuple, holding the color of text written on LMR
           widgets.
    """

    def __init__(self, left_img, mid_img, right_img, text_color):
        """Initialise.
           left_img, mid_img and right_img are the respective image file names.
        """

        # TODO: convert_alpha() should be called as soon as a display is available.

        self.left_img = pygame.image.load(left_img)

        self.mid_img = pygame.image.load(mid_img)

        self.right_img = pygame.image.load(right_img)

        self.text_color = text_color

        return

# Create some default styles
#
ORANGE_BUTTON_STYLE = LMRStyle(os.path.join(planes.gui.GFX_PATH,
                                            "button-orange-32px-l.png"),
                               os.path.join(planes.gui.GFX_PATH,
                                            "button-orange-32px-m.png"),
                               os.path.join(planes.gui.GFX_PATH,
                                            "button-orange-32px-r.png"),
                               (0, 0, 0))

WHITE_BUTTON_STYLE = LMRStyle(os.path.join(planes.gui.GFX_PATH,
                                           "button-white-32px-l.png"),
                              os.path.join(planes.gui.GFX_PATH,
                                           "button-white-32px-m.png"),
                              os.path.join(planes.gui.GFX_PATH,
                                           "button-white-32px-r.png"),
                              (0, 0, 0))

GREY_BUTTON_STYLE = LMRStyle(os.path.join(planes.gui.GFX_PATH,
                                          "button-grey-32px-l.png"),
                             os.path.join(planes.gui.GFX_PATH,
                                          "button-grey-32px-m.png"),
                             os.path.join(planes.gui.GFX_PATH,
                                          "button-grey-32px-r.png"),
                             (0, 0, 0))

BLACK_BUTTON_STYLE = LMRStyle(os.path.join(planes.gui.GFX_PATH,
                                           "button-black-32px-l.png"),
                              os.path.join(planes.gui.GFX_PATH,
                                           "button-black-32px-m.png"),
                              os.path.join(planes.gui.GFX_PATH,
                                           "button-black-32px-r.png"),
                              (255, 255, 255))

GREY_OPTION_STYLE = LMRStyle(os.path.join(planes.gui.GFX_PATH,
                                          "option-grey-32px-l.png"),
                             os.path.join(planes.gui.GFX_PATH,
                                          "option-grey-32px-m.png"),
                             os.path.join(planes.gui.GFX_PATH,
                                          "option-grey-32px-r.png"),
                             (0, 0, 0))

ORANGE_OPTION_STYLE = LMRStyle(os.path.join(planes.gui.GFX_PATH,
                                            "option-orange-32px-l.png"),
                               os.path.join(planes.gui.GFX_PATH,
                                            "option-orange-32px-m.png"),
                               os.path.join(planes.gui.GFX_PATH,
                                            "option-orange-32px-r.png"),
                               (0, 0, 0))

class LMRWidget:
    """Base class for fixed-height, flexible-width widgets with an LMR background.

       Additional attributes:

       LMRWidget.background
           A Pygame Surface, holding the rendered background for this widget.

       LMRWidget.style
           The LMRStyle instance for this widget.
    """

    def __init__(self, width, style):
        """Initialise LMRWidget.background from width and style given.

           width is the total widget width in pixels.

           style is an instance of LMRStyle.

           The height of the LMRWidget is taken from style.left_img.height.
        """

        if not isinstance(style, LMRStyle):

            msg = "'style' argument must be of class 'LMRStyle', not '{0}'"

            raise TypeError(msg.format(style.__class__.__name__))

        self.style = style

        # Compute dimensions
        #
        height = style.left_img.get_height()

        # We need it a couple of times
        #
        left_width = style.left_img.get_width()

        mid_width = width - left_width - style.right_img.get_width()

        # Create background image
        # Default to SRCALPHA.
        #
        self.background = pygame.Surface((width, height),
                                         flags = pygame.SRCALPHA).convert_alpha()

        self.background.blit(style.left_img, (0, 0))

        # Python: this creates a copy
        #
        x = left_width

        mid_img_width = style.mid_img.get_width()

        while x < (left_width + mid_width):

            self.background.blit(style.mid_img, (x, 0))

            x += mid_img_width

        # Clear area for right edge
        #
        self.background.fill((128, 128, 128, 0),
                             rect = pygame.Rect((left_width + mid_width, 0),
                                                style.right_img.get_size()))

        self.background.blit(style.right_img, (left_width + mid_width, 0))

        return

class LMRButton(LMRWidget, planes.gui.Button):
    """A planes.gui.Button with LMR background.
    """

    # TODO: Use Label font argument.

    def __init__(self, label, width, callback, style = GREY_BUTTON_STYLE):
        """Initialise the Button.

           label is the Text to be written on the button.

           callback is the function to be called with callback(Button) when the
           Button is clicked with the left mouse button.

           style is an instance of LMRStyle. If omitted, GREY_BUTTON_STYLE will be
           used.
        """

        # Initialise self.background
        #
        LMRWidget.__init__(self, width, style)

        # Now call base class.
        # This will also call redraw().
        #
        planes.gui.Button.__init__(self,
                                       label,
                                       self.background.get_rect(),
                                       callback)

        return

    def redraw(self):
        """Conditionally redraw the Button.
        """

        # Partly copied from Label.redraw()
        #
        if self.text != self.cached_text:

            # Copy, don't blit, taking care for transparency
            #
            self.image = self.background.copy()

            # Text is centered on rect.
            #
            fontsurf = planes.gui.FONTS.small_font.render(self.text,
                                                        True,
                                                        self.style.text_color)

            centered_rect = fontsurf.get_rect()

            # Get a neutral center of self.rect
            #
            centered_rect.center = pygame.Rect((0, 0), self.rect.size).center

            # Anticipate a drop shadow: move the text up a bit
            #
            centered_rect.move_ip(0, -1)

            self.image.blit(fontsurf, centered_rect)

            # Force redraw in render()
            #
            self.last_rect = None

            self.cached_text = self.text

        return

class LMROption(LMRWidget, planes.gui.Option):
    """A planes.gui.Option with LMR background.

       Additional attributes:

       LMROption.original_background
           The original background Surface.
    """

    def __init__(self, name, text, width, style):
        """Initialise the Label.

           text is the text to be written on the Label. If text is None, it is
           replaced by an empty string.

           width is the total widget width in pixels.

           style is an instance of LMRStyle.
        """

        # Initialise self.background
        #
        LMRWidget.__init__(self, width, style)

        self.original_background = self.background

        # Call base class. This calls through to planes.gui.Label.
        #
        planes.gui.Option.__init__(self, name, text, self.background.get_rect())

        return

    def redraw(self):
        """Unconditionally redraw the LMROption.
        """

        # Copied from LMRButton.redraw().
        # TODO: This is terribly inefficient. Refactor with flag check, like Label.

        # Copy, don't blit, taking care for transparency
        #
        self.image = self.background.copy()

        # Text is centered on rect.
        #
        fontsurf = planes.gui.FONTS.small_font.render(self.text,
                                                    True,
                                                    self.style.text_color)

        centered_rect = fontsurf.get_rect()

        # Get a neutral center of self.rect
        #
        centered_rect.center = pygame.Rect((0, 0), self.rect.size).center

        self.image.blit(fontsurf, centered_rect)

        # Force redraw in render()
        #
        self.last_rect = None

        return

    def clicked(self, button_name):
        """Highlight this option with a different LMR background and register as parent.selected.

           The Surface used for the highlight is
           LMROption.parent.highlighted_background. This only works if this
           LMROption is a subsurface of an LMROptionList.
        """

        if button_name == "left":

            for name in self.parent.subplanes_list:

                plane = self.parent.subplanes[name]
                plane.background = plane.original_background

                # Force redraw in render()
                #
                plane.last_rect = None

            self.background = self.parent.highlighted_background

            # Force redraw in render()
            #
            self.last_rect = None

            self.parent.selected = self

        return

class LMROptionList(planes.gui.OptionList):
    """A planes.gui.OptionList with LMROption elements.

       Options are LMROption subplanes of OptionList, named option0, option1,
       ..., optionN

       Please note that it is not possible to confirm a selection here. Use a
       wrapper like OptionSelector to accomplish that.

       Additional attributes:

       LMROptionList.highlighted_background
           A Pygame Surface, holding the background for the highlighted
           LMROption subplane.

       LMROptionList.selected
           The selected Option
    """

    def __init__(self, name, option_list, width, option_style = GREY_OPTION_STYLE, highlight_style = ORANGE_OPTION_STYLE):
        """Initialise the OptionList.

           option_list is a list of strings to be displayed as options.

           width is the total widget width in pixels.

           option_style is an optional instance of LMRStyle to be used for the
           LMROption subplanes. If it is omitted, GREY_OPTION_STYLE will be
           used.

           highlight_style is an optional instance of LMRStyle to be used for
           the highlighted LMROption subplane. If it is omitted,
           ORANGE_OPTION_STYLE will be used.
        """

        # This is a complete rewrite. We do not call the base class __init__()
        # on purpose.

        # Create a dummy LMRWidget
        #
        self.highlighted_background = LMRWidget(width, highlight_style).background

        # This is still a Container.
        # Create a transparent background. This will also disable the border.
        #
        planes.gui.Container.__init__(self,
                                          name,
                                          background_color = (128, 128, 128, 0))

        # Add options
        #
        for text in option_list:

            option = LMROption("option" + str(option_list.index(text)),
                               text,
                               width,
                               option_style)

            option.highlight = True

            self.sub(option)

        self.option0.background = self.highlighted_background
        self.selected = self.option0

        # Force redraw in render()
        #
        self.last_rect = None

        return

class LMRPlusMinusBox(planes.gui.PlusMinusBox):
    """A planes.gui.PlusMinusBox with LMRButtons.
       The value is accessible as PlusMinusBox.textbox.text
    """

    def __init__(self, name, charwidth, value = 0):
        """Initialise.

           charwidth is the width of the text field in characters.

           value, if given, is the initial numerical value.
        """

        # Copied from PlusMinusBox.__init__(), because we are lazy
        #
        minusbutton = LMRButton("minus", 32, self.minus_callback)

        minusbutton.down_click_callback = self.minus_callback

        minusbutton.text = "-"

        textbox = planes.gui.TextBox("textbox",
                                         pygame.Rect((minusbutton.rect.width, 0),
                                                     (planes.gui.PIX_PER_CHAR * charwidth,
                                                      minusbutton.rect.height)))

        textbox.down_click_callback = self.minus_callback
        textbox.up_click_callback = self.plus_callback

        plusbutton = LMRButton("plus", 32, self.plus_callback)

        plusbutton.up_click_callback = self.plus_callback

        plusbutton.text = "+"

        plusbutton.rect.left = minusbutton.rect.width + textbox.rect.width

        rect = pygame.Rect((0, 0),
                           (minusbutton.rect.width + textbox.rect.width + plusbutton.rect.width,
                            minusbutton.rect.height))

        # Call base class.
        # Leave optional arguments at their defaults.
        #
        planes.Plane.__init__(self, name, rect)

        # Make transparent
        #
        self.image = pygame.Surface(self.rect.size, flags = pygame.SRCALPHA)

        self.image.fill((128, 128, 128, 0))

        textbox.text = str(value)

        self.sub(minusbutton)
        self.sub(textbox)
        self.sub(plusbutton)

        return
