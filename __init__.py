import os
from libavg.AVGAppUtil import getMediaDir, createImagePreviewNode
from . import volumeControl

__all__ = ['apps']

def createPreviewNode(maxSize):
    filename = os.path.join(getMediaDir(__file__), 'preview.png')
    return createImagePreviewNode(maxSize, absHref = filename)

apps = (
        {'class': volumeControl.VolumeControl,
            'createPreviewNode': createPreviewNode},
        )
