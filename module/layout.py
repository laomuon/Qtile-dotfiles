from libqtile import layout
from libqtile.config import Match
from .kanagawa import colors


layout_theme = {
    # "border_width": 2,
    "border_focus": colors["highlight-background-color"],
    "border_normal": colors["background-color"],
    "margin": [5, 5, 5, 5],
}

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2, **layout_theme),
]
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
layouts.append(floating_layout)
