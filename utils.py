import settings

def width_prct(percentage):
    return (settings.WINDOW_WIDTH / 100) * percentage

def height_prct(percentage):
    return (settings.WINDOW_HEIGHT / 100) * percentage

def kill():
    with open(settings.FILE_EXPERIMENT_STATE, 'w') as f:
        f.write("killed")