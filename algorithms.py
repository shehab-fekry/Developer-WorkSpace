def on_enter(e):
    navButton['background'] = '#e16259'
    navButton['foreground'] = '#f8f8f8'
def on_leave(e):
    navButton['background'] = '#fdf5f2'
    navButton['foreground'] = '#e16259'


    navButton.bind('<Enter>', on_enter)
                navButton.bind('<Leave>', on_leave)