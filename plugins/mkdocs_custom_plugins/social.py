import os

from PIL import Image
from material.plugins.social.plugin import SocialPlugin

class CustomSocialPlugin(SocialPlugin):
    def on_config(self, config):
        self.docs_dir = config.docs_dir
        super().on_config(config)

    def _render_card_background(self, size, fill):
        if background := self.config.cards_layout_options.get("background_image"):
            image = Image.open(os.path.join(self.docs_dir, background))
            image = image.convert("RGBA")
            image = image.resize(size, Image.LANCZOS)

            if self.config.cards_layout_options.get("background_color"):
                image.alpha_composite(super()._render_card_background(size, fill))
        else:
            image = super()._render_card_background(size, fill)

        return image
    
    def _load_logo(self, config):
        theme = config.theme

        if logo := self.config.cards_layout_options.get("logo"):
            path = os.path.join(self.docs_dir, logo)
            _, extension = os.path.splitext(path)

            # Load SVG and convert to PNG
            if extension == ".svg":
                return self._load_logo_svg(path)

            # Load PNG, JPEG, etc.
            return Image.open(path).convert("RGBA")

        # Handle images (precedence over icons)
        if "logo" in theme:
            _, extension = os.path.splitext(theme["logo"])

            path = os.path.join(config.docs_dir, theme["logo"])

            # Allow users to put the logo inside their custom_dir (theme["logo"] case)
            if theme.custom_dir:
                custom_dir_logo = os.path.join(theme.custom_dir, theme["logo"])
                if os.path.exists(custom_dir_logo):
                    path = custom_dir_logo

            # Load SVG and convert to PNG
            if extension == ".svg":
                return self._load_logo_svg(path)

            # Load PNG, JPEG, etc.
            return Image.open(path).convert("RGBA")

        # Handle icons
        icon = theme["icon"] or {}
        if "logo" in icon and icon["logo"]:
            logo = icon["logo"]
        else:
            logo = "material/library"

        # Resolve path of package
        base = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "../.."
        ))

        path = f"{base}/.icons/{logo}.svg"

        # Allow users to put the logo inside their custom_dir (theme["icon"]["logo"] case)
        if theme.custom_dir:
            custom_dir_logo = os.path.join(theme.custom_dir, ".icons", f"{logo}.svg")
            if os.path.exists(custom_dir_logo):
                path = custom_dir_logo

        # Load icon data and fill with color
        return self._load_logo_svg(path, self.color["text"])