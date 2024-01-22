export const softwares = [
    {
        img : 'cell_analyzer.png',
        title : 'Cell analyzer HEK293/PYY/eYFP',
        text : 'Python based script for extraction and analysis of .tif formatted image files. The script will identify cells on a image based on set thresholds and parameters. From this a mask will be created to extract the intensity from up to three channels, here corresponding to signal from membrane stain (blue), yellow fluorescent protein (YFP, green) and Cy5/Atto655 (red).'
    },
    {
        img : 'common_tracking.png',
        title : 'Single Particle Tracking of Lipases',
        text : 'Python Script for analysing .tif movies of lipases diffusing on a surface. Code used to make data for Bohr, S. S.-R. et al. Scientific Reports, 2019'
    },
    {
        img : 'deepfret.png',
        title : 'DeepFRET',
        text : 'Rapid and automated single molecule FRET data classification using deep learning.'
    },
    {
        img : 'liposome_intensity_extraction.png',
        title : 'Extraction of liposome intensity',
        text : 'Python based script for extraction and analysis of .tif formatted image files. The script can extract the intensity from individual liposomes based in a changeable ROI size given initially and subtract local background'
    }
]