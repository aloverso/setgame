"""planes Graphical User Interface Module

   Copyright 2010-2013 by Florian Berger <fberger@florian-berger.de>

   Global variables:

   BACKGROUND_COLOR
       Defaults to (150, 150, 150).

   HIGHLIGHT_COLOR
       Defaults to (191, 95, 0).

   FONTS
       An instance of Fonts, a font manager.
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

# work started on 28. Oct 2010

# TODO: Make current Fabula Editor style the planes.gui default style
# TODO: Include some freely available game fonts

import planes
import pygame
import os.path
import sys
import unicodedata
import zipfile

BACKGROUND_COLOR = (150, 150, 150)
HIGHLIGHT_COLOR = (191, 95, 0)

PATH = None

# Check for cx_Freeze
#
if "frozen" in sys.__dict__.keys() and sys.frozen:

    PATH = sys.path[1]

else:
    PATH = os.path.dirname(__file__)

FONT_PATH = os.path.join(PATH, "fonts")
GFX_PATH = os.path.join(PATH, "gfx")

# Make sure resources are present
#
if not (os.path.exists(FONT_PATH) and os.path.exists(GFX_PATH)):

    print("WARNING: planes.gui: resource directories not found, extracting 'resources.zip' to '{0}'".format(PATH))

    if not os.path.exists(os.path.join(PATH, "resources.zip")):

        raise IOError("'resources.zip' not found. Please fix the installation of the 'planes' package.")

    zf = zipfile.ZipFile(os.path.join(PATH, "resources.zip"))

    # It would be way better to read files directly from the zip file.
    # But, contrary to the documentation, this is currently unsupported
    # by PyGame. See "Segfault on loading font from StringIO" at
    # http://blog.gmane.org/gmane.comp.python.pygame/month=20120101
    #
    zf.extractall(PATH)

    zf.close()

# TODO: still necessary after extracting zip?
#
# # Check for cx_Freeze
# #
# if "frozen" in sys.__dict__.keys() and sys.frozen:
#
#     FONT_PATH = sys.path[1]

# Pixels per character, for width estimation of text renderings
# TODO: merge with Fonts manager
#
PIX_PER_CHAR = 8

class Fonts:
    """A font manager.

       Attributes:

       Fonts.font_names
           A list of font names that should be available. Use Fonts.by_name()
           to load and return a pygame.font.Font instance. This will raise an
           exception if the font is not available.

       Fonts.font_sizes
           A list of font sizes that should be available. Use Fonts.by_size()
           to load and return a pygame.font.Font instance. This will raise an
           exception if the font is not available.

       Fonts.fonts_by_name
           A dict mapping names of loaded fonts to pygame.font.Font instances.
           Using Fonts.by_name() instead of this dict is recommended, as it
           will load missing fonts.

       Fonts.fonts_by_size
           A dict mapping pixel sizes of loaded fonts to pygame.font.Font
           instances. Using Fonts.by_size() instead of this dict is recommended,
           as it will load missing fonts.

       Fonts.big_font
           A default pygame.font.Font instance, large pointsize. Always
           available.

       Fonts.small_font
           A default pygame.font.Font instance, small pointsize. Always
           available.

       Fonts.bold_font
           A default pygame.font.Font instance, bold face. Always available.
    """

    def __init__(self):
        """Initialise.
        """

        # Initialise the font module. This can safely be called more than once.
        #
        pygame.font.init()

        # {<font name> : (<font file>, <pixel size>)}
        #
        self._font_dict = {"04B-08" : ("04B_08__.ttf", 8),
                           "04B-19" : ("04B_19__.ttf", 14),
                           "BitLow" : ("bitlow.ttf", 9),
                           "Tempesta Seven Compressed Bold" :
                               ("pf_tempesta_seven_compressed_bold.ttf", 8),
                           "Tempesta Seven Extended Bold" :
                               ("pf_tempesta_seven_extended_bold.ttf", 8),
                           "Tempesta Seven" : ("pf_tempesta_seven.ttf", 8),
                           "Sans Nouveaux" : ("px_sans_nouveaux.ttf", 8),
                           "Silkscreen" : ("slkscr.ttf", 8),
                           "Bitstream Vera Sans Bold" : ("VeraBd.ttf", 12),
                           "Bitstream Vera Sans" : ("Vera.ttf", 12)}

        self.font_names = list(self._font_dict.keys())

        self.font_sizes = [file_size[1] for file_size in self._font_dict.values()]

        self.fonts_by_name = {}

        self.fonts_by_size = {}

        # Initialise default font instances.
        # Taken from fabula.PygameUserInterface.
        #
        try:
            # Small
            #
            small_font_file = os.path.join(FONT_PATH,
                                           self._font_dict["Sans Nouveaux"][0])

            # Use multiple of default size
            #
            size = self._font_dict["Sans Nouveaux"][1] * 1

            self.small_font = pygame.font.Font(small_font_file, size)

            self.fonts_by_name["Sans Nouveaux"] = self.small_font
            self.fonts_by_size[size] = self.small_font

            # Big
            #
            big_font_file = os.path.join(FONT_PATH,
                                         self._font_dict["Sans Nouveaux"][0])

            # Use multiple of default size
            #
            size = self._font_dict["Sans Nouveaux"][1] * 4

            self.big_font = pygame.font.Font(big_font_file, size)

            self.fonts_by_size[size] = self.big_font

            # Bold
            #
            bold_font_file = os.path.join(FONT_PATH,
                                          self._font_dict["Bitstream Vera Sans Bold"][0])

            self.bold_font = pygame.font.Font(bold_font_file,
                                              self._font_dict["Bitstream Vera Sans Bold"][1])

            self.fonts_by_name["Bitstream Vera Sans Bold"] = self.bold_font
            self.fonts_by_size[self._font_dict["Bitstream Vera Sans Bold"][1]] = self.bold_font

        except:
            # TODO: log used font: pygame.font.get_default_font()
            #print("Could not load {0}".format(os.path.join(os.path.dirname(__file__), "Vera.ttf")))
            self.big_font = pygame.font.Font(None, 40)
            self.small_font = self.bold_font = pygame.font.Font(None, 20)

        return

    def by_name(self, font_name, scale = 1):
        """Return a pygame.font.Font instance identified by font_name.

           scale is a scale factor >= 1. If omitted, the default size will
           be used.

           Fonts.font_names has a list of font names that should be available.

           This method will raise a KeyError if the font can not be found.
        """

        font = None

        # Always create a new font instance to honour the scale argument.
        # This effectively changes the scale of an already loaded font.
        #
        if font_name in self.font_names:

            size = self._font_dict[font_name][1] * int(scale)

            font = pygame.font.Font(os.path.join(FONT_PATH,
                                                 self._font_dict[font_name][0]),
                                    size)

            self.fonts_by_name[font_name] = font

            # Overwrite possibly existing font.
            #
            self.fonts_by_size[size] = font

        else:
            raise KeyError("cannot load unknown font: '{0}'".format(font_name))

        return font

    def by_size(self, size):
        """Return a pygame.font.Font instance identified by size.

           Fonts.font_sizes has a list of font sizes that should be available.

           This method will raise a KeyError if the font can not be found.
        """

        # TODO: it is undefined which font will be returned, as it depends on which font of that size has been loaded. Make this deterministic?

        font = None

        if size in self.fonts_by_size.keys():

            font = self.fonts_by_size[size]

        elif size in self.font_sizes:

            # There is some unloaded font of that size.
            #
            for font_name in self._font_dict.keys():

                if self._font_dict[font_name][1] == size:

                    font = pygame.font.Font(os.path.join(FONT_PATH,
                                                         self._font_dict[font_name][0]),
                                            self._font_dict[font_name][1])

                    self.fonts_by_name[font_name] = font

                    # Overwrite possibly existing font.
                    #
                    self.fonts_by_size[size] = font

        else:
            raise KeyError("could not find a font for size '{0}'".format(size))

        return font

# Create a singleton fonts manager.
#
FONTS = Fonts()

def draw_border(plane, color):
    """Draw a border around plane.
    """
    pygame.draw.lines(plane.image,
                      color,
                      True,
                      ((0, 0),
                       (plane.rect.width - 1, 0),
                       (plane.rect.width - 1, plane.rect.height - 1),
                       (0, plane.rect.height - 1)))

    return

class Label(planes.Plane):
    """A planes.Plane which displays a text.

       Additional attributes:

       Label.text
           The text to be written on the Label

       Label.cached_text
           Cache to catch changes

       Label.background_color
           The original background color for this Label

       Label.current_color
           The current background color

       Label.cached_color
           A cache for color changes

       Label.text_color
           The text color, initially (0, 0, 0).

       Label.font
           The PyGame.font.Font instante used for this Label.
    """

    def __init__(self, name, text, rect,
                 background_color = None,
                 text_color = (0, 0, 0),
                 font = FONTS.small_font):
        """Initialise the Label.
           text is the text to be written on the Label. If text is None, it is
           replaced by an empty string.
        """

        # Call base class init
        #
        planes.Plane.__init__(self, name, rect, draggable = False, grab = False)

        if text is not None:

            self.text = text

        else:
            self.text = ""

        self.cached_text = None

        self.background_color = self.cached_color = self.current_color = BACKGROUND_COLOR

        if background_color is not None:

            self.background_color = self.cached_color = self.current_color = background_color

            # If there is an alpha channel, replace by a SRCALPHA Surface
            #
            if len(self.background_color) == 4:

                self.image = pygame.Surface(self.rect.size,
                                            flags = pygame.SRCALPHA)

        self.text_color = text_color

        self.font = font

        self.redraw()

        return

    def update(self):
        """Renew the text on the label, then call the base class method.
        """

        self.redraw()

        planes.Plane.update(self)

        return

    def redraw(self):
        """Redraw the Label if necessary.
        """

        if (self.text != self.cached_text
            or self.current_color != self.cached_color):

            self.image.fill(self.current_color)

            # Text is centered on rect.
            #
            fontsurf = self.font.render(self.text, True, self.text_color)

            centered_rect = fontsurf.get_rect()

            # Get a neutral center of self.rect
            #
            centered_rect.center = pygame.Rect((0, 0), self.rect.size).center

            self.image.blit(fontsurf, centered_rect)

            # Force redraw in render()
            #
            self.last_rect = None

            self.cached_text = self.text
            self.cached_color = self.current_color

        return

class OutlinedText(Label):
    """A Label with outlined text and a transparent background.

       Additional attributes:

       OutlinedText.text_color
          A tuple (R, G, B) holding the color of the text.
    """

    # TODO: Use Label font argument.

    def __init__(self, name, text,
                 text_color = (255, 255, 255), font = None):
        """Initialise the OutlinedText.
           text is the text to be written on the Label. If text is None, it is
           replaced by an empty string.
        """

        # Use a dummy rect, the final rect will be set in redraw().
        #
        rect = pygame.rect.Rect((0, 0), (0, 0))

        # Call the base class.
        #
        if font is None:

            Label.__init__(self,
                           name,
                           text,
                           rect,
                           text_color = text_color)

        else:
            Label.__init__(self,
                           name,
                           text,
                           rect,
                           text_color = text_color,
                           font = font)

        return

    def redraw(self):
        """Redraw the Label if necessary.
           The new Label will have the same rect center as the old Label.
        """

        if self.text != self.cached_text:

            # Outlined text rendering inspired by Pete Shinners
            # (http://www.pygame.org/pcr/hollow_outline/index.php)
            # and Stackoverflow
            # (http://stackoverflow.com/questions/1109498/whats-a-good-way-to-render-outlined-fonts).

            # Black outline
            #
            font_surface = self.font.render(self.text,
                                            True,
                                            (0, 0, 0))

            target_surface = pygame.Surface(font_surface.get_rect().inflate(2, 2).size,
                                            flags = pygame.SRCALPHA)

            target_surface.blit(font_surface, (0, 0))
            target_surface.blit(font_surface, (1, 0))
            target_surface.blit(font_surface, (2, 0))

            target_surface.blit(font_surface, (0, 1))
            target_surface.blit(font_surface, (2, 1))

            target_surface.blit(font_surface, (0, 2))
            target_surface.blit(font_surface, (1, 2))
            target_surface.blit(font_surface, (2, 2))

            # Center
            #
            font_surface = self.font.render(self.text,
                                            True,
                                            self.text_color)

            target_surface.blit(font_surface, (1, 1))

            # Save current center
            #
            center = self.rect.center

            # Set new rect and image.
            #
            self.image = target_surface
            self.rect = target_surface.get_rect()

            # Restore center, avoiding an uninitialised value
            #
            if center != (0, 0):

                self.rect.center = center

            # Force redraw in render()
            #
            self.last_rect = None

            self.cached_text = self.text

        return

class Button(Label):
    """A planes plane which displays a text and reacts on mouse clicks.

       Additional attributes:

       Button.callback
           The callback function to be called with callback(Button) upon
           clicking.

       Button.clicked_counter
           Counted down when the button is clicked and displays a different color
    """

    # TODO: Use Label font argument.

    def __init__(self, label, rect, callback, background_color = None, text_color = (0, 0, 0)):
        """Initialise the Button.
           label is the Text to be written on the button.
           rect is an instance of pygame.Rect giving the dimensions.
           callback is the function to be called with callback(Button) when the
           Button is clicked with the left mouse button.
        """

        # name is the alphanumeric-only-lower case-version of label
        #
        name = ''.join(filter(str.isalnum, label)).lower()

        if not name:
            raise Exception("Invalid Button name '{0}': it must contain at least one alphanumeric character.".format(label))

        if background_color is None:

            background_color = BACKGROUND_COLOR

        # Call base class init
        #
        Label.__init__(self, name, label, rect, background_color, text_color)

        # Overwrite Plane base class attributes
        #
        self.left_click_callback = callback
        self.highlight = True

        self.clicked_counter = 0

        self.redraw()

        return

    def redraw(self):
        """Redraw the Button.
        """

        # First redraw base Label
        #
        Label.redraw(self)

        # Embossed button with a 1px border.
        # TODO: this is always redrawn. Replace with a condition.

        self.image.lock()

        # width is 1px by default
        #
        pygame.draw.lines(self.image,
                          [int(color / 2) for color in self.background_color],
                          False,
                          [(1, self.rect.height - 1),
                           (self.rect.width - 1, self.rect.height - 1),
                           (self.rect.width - 1, 1)])

        pygame.draw.lines(self.image,
                          [int(color * 1.33) for color in self.background_color],
                          False,
                          [(0, self.rect.height - 2),
                           (0, 0),
                           (self.rect.width - 2, 0)])

        self.image.unlock()

        return

    def update(self):
        """Change color if clicked, then call the base class method.
        """

        if self.clicked_counter:

            self.clicked_counter = self.clicked_counter - 1

            if not self.clicked_counter:

                # Just turned zero, restore original background
                #
                self.current_color = self.background_color

        Label.update(self)

        return

    def clicked(self, button_name):
        """Plane standard method, called when there is a MOUSEDOWN event on this plane.
           Changes the Button color for some frames and calls the base class implementation.
        """

        if button_name == "left":

            self.clicked_counter = 4

            # Half-bright
            #
            self.current_color = list(map(lambda i: int(i * 0.5), self.current_color))

            self.redraw()

        # Call base class implementation which will call the callback
        #
        Label.clicked(self, button_name)

        return

class Container(planes.Plane):
    """A Container for Planes.
       If a subplane is added via sub(), the container places it below any existing
       subplanes and resizes itself to fit the width and height of the subplanes.

       Additional attributes:

       Container.padding
           Space between subplanes and border, in pixels

       Container.background_color
           The original background color for this Container
    """

    def __init__(self, name, padding = 0, background_color = None):
        """Initialise.
           Container.image is initialised to a 0x0 px Surface.
        """

        # Call base class
        #
        planes.Plane.__init__(self, name, pygame.Rect((0, 0), (0, 0)))

        self.padding = padding

        self.background_color = BACKGROUND_COLOR

        if background_color is not None:

            self.background_color = background_color

        return

    def redraw(self):
        """Redraw Container.image from the dimensions in Containter.rect.
           This also creates a new Container.rendersurface.
        """

        # Create Surface with background color
        #
        if len(self.background_color) == 4:

            self.image = pygame.Surface(self.rect.size,
                                        flags = pygame.SRCALPHA)

        else:

            self.image = pygame.Surface(self.rect.size)

        self.image.fill(self.background_color)

        # Only draw a border if there is no alpha channel.
        #
        if len(self.background_color) == 3:

            draw_border(self, (0, 0, 0))

        # Create a new rendersurface
        #
        self.rendersurface = self.image.copy()

        return

    def sub(self, plane):
        """Resize the container, update the position of plane and add it as a subplane.
        """

        # First add the subplane by calling the base class method.
        # This also cares for re-adding an already existing subplane.
        #
        planes.Plane.sub(self, plane)

        # Containers have a 1px black border. Observe this when calculating width
        # and height.
        # Existing subplanes are already incorporated in self.rect.

        # Conditionally fit new width
        #
        if plane.rect.width > self.rect.width - 2 * self.padding - 2:

            self.rect.width = plane.rect.width + 2 * self.padding + 2

        # Mandatory fit new height, observe padding
        #
        if not self.rect.height:

            # No subplanes yet

            plane.rect.topleft = (0, 1 + self.padding)

            self.rect.height = plane.rect.height + 2 * self.padding + 2

        else:
            plane.rect.topleft = (0, self.rect.height - 1)

            self.rect.height = self.rect.height + plane.rect.height + self.padding

        # Re-center all subplanes.
        #
        for name in self.subplanes_list:

            rect = self.subplanes[name].rect
            rect.centerx = int(self.rect.width / 2)

        self.redraw()

        return

    def remove(self, plane_identifier):
        """Remove the subplane, then reposition remaining subplanes and resize the container.
        """

        # Accept Plane name as well as Plane instance
        #
        if isinstance(plane_identifier, planes.Plane):

            name = plane_identifier.name

        else:
            name = plane_identifier

        # Save the height of the removed plane
        #
        height_removed = self.subplanes[name].rect.height + self.padding

        planes.Plane.remove(self, name)

        # Reposition remaining subplanes.
        #
        top = 1 + self.padding

        for name in self.subplanes_list:
            rect = self.subplanes[name].rect
            rect.top = top
            top = top + rect.height + self.padding

        # Now shrink and redraw.
        #
        self.rect.height = self.rect.height - height_removed

        # Find widest subplane.
        # Partly copied from Container.sub().
        #
        self.rect.width = 4

        for plane in self.subplanes.values():

            if plane.rect.width > self.rect.width - 2 * self.padding - 2:

                self.rect.width = plane.rect.width + 2 * self.padding + 2

        self.redraw()

        return

    def remove_all(self):
        """Remove all subplanes and shrink accordingly.
        """

        # Cave: loop while modifying loop item source. Create a new list.
        #
        for name in list(self.subplanes_list):

            self.remove(name)

        return

class Option(Label):
    """A subclass of Label which handles mouseclicks, to be used in an OptionList.
    """

    def clicked(self, button_name):
        """Highlight this option and register as parent.selected.
        """

        if button_name == "left":

            for name in self.parent.subplanes_list:

                plane = self.parent.subplanes[name]
                plane.current_color = plane.background_color

                # Force redraw in render()
                #
                plane.last_rect = None

            self.current_color = HIGHLIGHT_COLOR

            # Force redraw in render()
            #
            self.last_rect = None

            self.parent.selected = self

        return

class OptionList(Container):
    """A list of options to select from.

       Options are subplanes of OptionList, named option0, option1, ..., optionN

       Please note that it is not possible to confirm a selection here. Use a
       wrapper like OptionSelector to accomplish that.

       Additional attributes:

       OptionList.selected
           The selected Option
    """

    def __init__(self, name, option_list, width = 200, lineheight = 30):
        """Initialise the OptionList.
           option_list is a list of strings to be displayed as options.
        """

        # Call base class init
        #
        Container.__init__(self, name)

        # Add options
        #
        for text in option_list:

            option = Option("option" + str(option_list.index(text)),
                            text,
                            pygame.Rect((0, 0), (width, lineheight)))

            option.highlight = True

            self.sub(option)

        self.option0.current_color = HIGHLIGHT_COLOR
        self.selected = self.option0

        return

class OptionSelector(Container):
    """An OptionSelector wraps an OptionList and an OK button, calling a callback when a selection is confirmed.
    """

    def __init__(self, name, option_list, callback, width = 200, lineheight = 30, background_color = None):
        """Initialise the OptionSelector.
           option_list is a list of strings to be displayed as options.
           callback is a function to be called with the selected Option instance
           as argument once the selection is made.
        """

        # Call base class init
        #
        Container.__init__(self,
                           name,
                           padding = 5,
                           background_color = background_color)

        # TODO: copied from Button.__init__. Maybe inherit from a third class 'Callback'?
        #
        self.callback = callback

        # Add options and OK button
        #
        ol = OptionList("option_list",
                        option_list,
                        width,
                        lineheight)

        self.sub(ol)

        button = Button("OK",
                        pygame.Rect((0, 0), (width, lineheight)),
                        self.selection_made)

        self.sub(button)

        return

    def selection_made(self, plane):
        """Button callback called when the user confirmed an option from the list.
           Calls OptionSelector.callback(self.option_list.selected) and destroys the OptionSelector.
        """

        self.callback(self.option_list.selected)

        self.destroy()

        return

class OkBox(Container):
    """A box which displays a message and an OK button.
       It is destroyed when OK is clicked.
       The message will be wrapped at newline characters.
    """

    def __init__(self, message):
        """Initialise.
        """

        # Base class __init__()
        # We need a unique random name an just use this instance's id.
        # TODO: prefix with some letters to make it usable via attribute calls
        #
        Container.__init__(self, str(id(self)), padding = 5)

        lines = message.split("\n")

        for line_no in range(len(lines)):

            self.sub(Label("message_line_{0}".format(line_no),
                           lines[line_no],
                           pygame.Rect((0, 0), (len(lines[line_no]) * PIX_PER_CHAR, 30))))

        self.sub(Button("OK", pygame.Rect((0, 0), (50, 30)), self.ok))

        return

    def ok(self, plane):
        """Button clicked callback which destroys the OkBox.
        """

        self.destroy()

        return

class TextBox(Label):
    """A box where the user can type text.

       To actually receive key events, the TextBox must be registered with the
       Display using Display.key_sensitive(TextBox).

       Attributes:

       TextBox.text
           Standard Label attribute, holding the text typed so far.

       TextBox.active
           Boolean flag whether this TextBox is active, initally False.
    """

    # TODO: Use Label font argument.

    def __init__(self, name, rect, return_callback = None, background_color = (250, 250, 250)):
        """Initialise the TextBox.
           If return_callback is given, return_callback(TextBox.text) will be
           called when [RETURN] is pressed.
        """

        # TODO: why call callback with string, not Plane? This is inconsistent.

        # Label.__init__() calls redraw() which needs self.active.
        #
        self.active = False

        # Call base class
        #
        Label.__init__(self, name, None, rect, background_color)

        self.return_callback = return_callback

        return

    def keydown(self, keydown_event):
        """If printable, add keydown_event.unicode to self.text.
        """

        # We can not use Python 3's str.isprintable() for Python 2 compatibility
        # reasons. As a workaround, we check the Unicode category of the input.
        # See http://www.unicode.org/Public/5.1.0/ucd/UCD.html#General_Category_Values
        #
        if len(keydown_event.unicode) and unicodedata.category(keydown_event.unicode)[0] in "LNPSZ":

            self.text = self.text + keydown_event.unicode

        elif keydown_event.key == pygame.K_BACKSPACE:

            self.text = self.text[:-1]

        elif keydown_event.key == pygame.K_RETURN and self.return_callback is not None:

            # Deactivate to lose the cursor
            #
            self.deactivate()

            self.return_callback(self.text)

        return

    def activate(self):
        """Call to show the user that the TextBox is ready for input.
           Sets TextBox.active to True.
        """

        self.active = True

        self.redraw(force = True)

        return

    def deactivate(self):
        """Call to show the user that the TextBox no longer accepts input.
           Sets TextBox.active to False.
        """

        self.active = False

        self.redraw(force = True)

        return

    def redraw(self, force = False):
        """Redraw the TextBox if necessary.
           If the TextBox is active, display a cursor behind the text.
        """

        if (self.text != self.cached_text
            or self.current_color != self.cached_color
            or force):

            self.image.fill(self.current_color)

            # Give background for speedup.
            # Clever use of a dict to avoid an 'if'! :-)
            #
            fontsurf = FONTS.small_font.render(self.text + {True: "|", False: ""}[self.active],
                                         True,
                                         (0, 0, 0),
                                         self.current_color)

            # Text is left-aligned on rect, except when it is larger than the
            # Label, in which case it is right-aligned.
            #
            if fontsurf.get_rect().width > self.rect.width:

                self.image.blit(fontsurf, (self.rect.width - fontsurf.get_rect().width, 0))

            else:
                self.image.blit(fontsurf, (0, 0))

            # Force redraw in render()
            #
            self.last_rect = None

            self.cached_text = self.text
            self.cached_color = self.current_color

        return

class GetStringDialog(Container):
    """A combination of Container, Label, TextBox and Button that asks the user for a string.

       Additional attributes:

       GetStringDialog.callback
           The callback to be called callback(string) when the input is confirmed.
    """

    # TODO: this could be merged with OkBox into a class "ConfirmBox"

    def __init__(self, prompt, callback, display):
        """Initialise.
           callback will be called callback(GetStringDialog.textbox.text)
           after the GetStringDialog is destroyed. It should call render()
           and flip the display to remove the GetStringDialog from the screen.
           display.key_sensitive() will be used to register the TextBox of this
           dialog.
        """

        # Initialise container
        #
        Container.__init__(self, "get_string_dialog", padding = 5)

        self.callback = callback

        self.sub(Label("prompt", prompt, pygame.Rect((0, 0), (200, 30))))

        textbox = TextBox("textbox",
                          pygame.Rect((0, 0), (200, 30)),
                          return_callback = self.return_key)

        self.sub(textbox)

        display.key_sensitive(textbox)

        self.sub(Button("OK",
                        pygame.Rect((0, 0), (90, 30)),
                        self.ok))

        return

    def ok(self, plane):
        """Button callback to destroy the GetStringDialog and call GetStringDialog.callback(string).
        """

        # Deactivate to lose the cursor
        #
        self.textbox.deactivate()

        callback = self.callback
        string = self.textbox.text

        self.destroy()

        callback(string)

        return

    def return_key(self, text):
        """Return key callback to destroy the GetStringDialog and call GetStringDialog.callback(string).
        """
        # TODO: Copied from above. Can these be made into one?

        callback = self.callback

        self.destroy()

        callback(text)

        return

class ScrollingPlane(planes.Plane):
    """This class implements a fixed-dimension plane with a scroll bar to scroll its content plane.
       Subplane structure:

       ScrollingPlane
       |
       +---content
       |   |
       |   +---content_plane from __init__()
       |
       +---scrollbar_container
           |
           +---scrollbar
    """

    def __init__(self, name, rect, content_plane, draggable = False, grab = False, clicked_callback = None, dropped_upon_callback = None):
        """Initalise.
           rect states the dimensions without the scroll bar.
        """

        rect.width = rect.width + 12

        # Call base class
        #
        planes.Plane.__init__(self, name, rect, draggable, grab, clicked_callback, dropped_upon_callback)

        self.image.fill(BACKGROUND_COLOR)

        self.sub(planes.Plane("content", pygame.Rect((0, 0),
                                                         (self.rect.width - 12, self.rect.height))))

        content_plane.rect.topleft = (0, 0)
        self.content.sub(content_plane)

        scrollbar_container = planes.Plane("scrollbar_container",
                                               pygame.Rect((self.rect.width - 12, 0),
                                                           (12, self.rect.height)))

        scrollbar_container.image.fill(BACKGROUND_COLOR)
        draw_border(scrollbar_container, (0, 0, 0))

        def scrollbar_container_clicked(plane):
            """Clicked callback which repositions the content Plane and scrollbar according to the y-position of the mouse.
            """

            x, y = pygame.mouse.get_pos()

            new_y = y - self.rect.top

            # Align scrollbar at bottom
            #
            if new_y > self.rect.height - self.scrollbar_container.scrollbar.rect.height - 2:
                new_y = self.rect.height - self.scrollbar_container.scrollbar.rect.height - 2

            self.scrollbar_container.scrollbar.rect.top = new_y

            content_plane = self.content.subplanes[self.content.subplanes_list[0]]
            content_plane.rect.top = int(0 - new_y / self.rect.height * content_plane.rect.height)

            # Invalidate last_image_id to trigger a redraw
            # TODO: changing content_plane.rect.top above should invalidate last_rect, why is this necessary?
            #
            content_plane.last_image_id = None

            return

        scrollbar_container.left_click_callback = scrollbar_container_clicked

        self.sub(scrollbar_container)

        # Scrollbar height reflects the proportions
        #
        self.scrollbar_container.sub(planes.Plane("scrollbar", pygame.Rect((2, 2),
                                                                          (8, int(self.rect.height / content_plane.rect.height * self.rect.height)))))

        # Half-bright color taken from Button.clicked()
        #
        self.scrollbar_container.scrollbar.image.fill(list(map(lambda i : int(i * 0.5), BACKGROUND_COLOR)))

        return

class PlusMinusBox(planes.Plane):
    """This class implements a TextBox with plus and minus buttons attached, to change a numerical value.
       The value is accessible as PlusMinusBox.textbox.text
    """

    def __init__(self, name, charwidth, value = 0):
        """Initialise.
           charwidth is the width of the text field in characters.
           value, if given, is the initial numerical value.
        """

        minusbutton = Button("minus",
                             pygame.Rect((0, 0), (PIX_PER_CHAR, PIX_PER_CHAR * 2)),
                             self.minus_callback)

        minusbutton.down_click_callback = self.minus_callback

        minusbutton.text = "-"

        textbox = TextBox("textbox",
                          pygame.Rect((minusbutton.rect.width, 0),
                                      (PIX_PER_CHAR * charwidth, PIX_PER_CHAR * 2)))

        textbox.down_click_callback = self.minus_callback
        textbox.up_click_callback = self.plus_callback

        plusbutton = Button("plus",
                            pygame.Rect((minusbutton.rect.width + textbox.rect.width, 0),
                                        (PIX_PER_CHAR, PIX_PER_CHAR * 2)),
                            self.plus_callback)

        plusbutton.up_click_callback = self.plus_callback

        plusbutton.text = "+"

        rect = pygame.Rect((0, 0),
                           (minusbutton.rect.width + textbox.rect.width + plusbutton.rect.width,
                            PIX_PER_CHAR * 2))

        # Call base class.
        # Leave optional arguments at their defaults.
        #
        planes.Plane.__init__(self, name, rect)

        textbox.text = str(value)

        self.sub(minusbutton)
        self.sub(textbox)
        self.sub(plusbutton)

        return

    def minus_callback(self, Plane):
        """Callback when minus is clicked.
        """

        self.textbox.text = str(int(self.textbox.text) - 1)

        self.textbox.redraw()

        return

    def plus_callback(self, Plane):
        """Callback when plus is clicked.
        """

        self.textbox.text = str(int(self.textbox.text) + 1)

        self.textbox.redraw()

        return

class FadingContainer(Container):
    """A Container that, once visible, will fade out and destroy itself.

       Additional attributes:

       FadingContainer.display_duration
           The number of calls to update() that the FadingContainer will be
           displayed. Will be decremented in FadingContainer.update().

       FadingContainer.alpha_steps
           A list of decreasing alpha values to be applied to the
           Surface of the FadingContainer, computed from fade_duration
           in FadingContainer.__init__().
    """

    # TODO: Couldn't this be an abstract add-in for all kinds of GUI elements? So just inheriting from e.g. FadingElement would add this behaviour? Or a decorator like @Fading?

    def __init__(self,
                 name,
                 display_duration,
                 fade_duration,
                 padding = 0,
                 background_color = None):
        """Initialise.

           display_duration is the number of calls to update() that the
           FadingContainer will be displayed.

           fade_duration is the number of calls to update() that the
           FadingContainer will take to fade out.
        """

        # Call base class
        #
        Container.__init__(self, name, padding, background_color)

        self.display_duration = display_duration

        self.alpha_steps = list(range(255, 0, -int(255 / fade_duration)))

        return

    def update(self):
        """Call Plane.update(), then decrement FadingContainer.display_duration and destroy when len(self.alpha_steps) has reached zero.
        """

        # Call base class
        #
        planes.Plane.update(self)

        if self.display_duration > 0:

            self.display_duration -= 1

        else:

            if not len(self.alpha_steps):

                self.destroy()

        return

    def render(self, displayrect = None):
        """Call Plane.render(), the pop the first value from self.alpha_steps and apply it as alpha.
        """

        # Call base class
        #
        planes.Plane.render(self, displayrect)

        if self.display_duration <= 0:

            # Only fade if the fade is actually visible, i.e. no per-pixel alpha.
            # TODO: Implement fading for Surfaces with per-pixel alpha. Replace transparent pixels with transparent color, convert the Surface to a no-SRCALPHA Surface.
            #
            if self.rendersurface.get_flags() & pygame.SRCALPHA:

                # Will be caught by update()
                #
                self.alpha_steps = []

            else:
                self.rendersurface.set_alpha(self.alpha_steps.pop(0))

        # Always return True to force a redraw
        #
        return True

class ProgressBar(planes.Plane):
    """A horizontal progress bar, filling from left to right.
       Additional attributes:

       ProgressBar.percent
           An integer 0..100.

       ProgressBar.text
           text is a string to be rendered on top of the bar. Initially an
           empty string.

       ProgressBar.label
           A Label instance displaying ProgressBar.text.

       ProgressBar.color
           color is a tuple (R, G, B) giving the color of the bar.

       ProgressBar.background_color
           background_color is a tuple (R, G, B) giving the background color of
           the bar.
    """

    def __init__(self, name, rect, percent, text = "", color = (0, 0, 255),
                 background_color = None):
        """Initialise.

           percent must be an integer 0..100.

           text is a string to be rendered on top of the bar.

           color is a tuple (R, G, B) giving the color of the bar.

           background_color is a tuple (R, G, B) giving the background color of
           the bar.
        """

        # Call base class
        #
        planes.Plane.__init__(self, name, rect)

        self.percent = percent

        self.text = text

        # By default, make the label as big as the bar
        #
        self.label = Label("{0}-label".format(self.name), self.text,
                           pygame.Rect((0, 0), self.rect.size),
                           background_color = (128, 128, 128, 0),
                           text_color = (255, 255, 255))

        self.sub(self.label)

        self.color = color

        self.background_color = background_color

        return

    def update(self):
        """Update ProgressBar.label.text to ProgressBar.text, redraw, then call the base class method.
        """

        self.label.text = self.text

        self.redraw()

        planes.Plane.update(self)

        return

    def redraw(self, displayrect = None):
        """Update ProgressBar.image to reflect ProgressBar.percent.
        """

        # Background
        #
        if self.background_color is None:

            self.image = pygame.Surface(self.rect.size, flags = pygame.SRCALPHA)

        else:
            self.image.fill(self.background_color)

        # Actual bar
        # Leave 1px border.
        #
        width = int((self.percent / 100.0) * (self.rect.width - 2))

        self.image.fill(self.color, pygame.Rect((1, 1),
                                                (width, self.rect.height - 2)))

        # Force redraw in render()
        #
        self.last_image_id = None

        return
