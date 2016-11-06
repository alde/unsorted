import os
import re
import shutil
import logging

from . import NAS_SHOWS

logger = logging.getLogger(__name__)

showLocations = [NAS_SHOWS]
videoTypes = ['.avi', '.mkv', '.wmv', '.mp4']


def adoptionCandidates(basedir, file):
    dirs = filter(lambda x : os.path.isdir(os.path.join(basedir, x)), os.listdir(basedir))
    if os.path.isdir(file):
        logger.error('%s is a directory. Aborting' % file)
        return []

    (filepath, filename) = os.path.split(file)

    filename = filename.upper()

    ignoredPhrases = ['-','_']

    candidates = []
    for dir in dirs:
        dirParts = dir.split()
        score = 0
        requiredScore = 0

        for part in dirParts:
            part = part.upper()

            if ignoredPhrases.count(part) > 0:
                continue

            requiredScore = requiredScore + 1
            if filename.startswith("."):
                continue

            if filename.find(part) >= 0:
                score = score + 1

        if score == requiredScore:
            candidates.append( (os.path.join(basedir, dir), score) )

    return candidates


def getSeasonNumber(filename):
    patterns = [
        '.*S(\d+)E(\d+).*',
        '(\d+)x(\d+).*'
    ]
    pattern2 = '\.(\d)(\d)(\d)(\d).*'
    pattern3 = '\.(\d)(\d)(\d).*'

    for pattern in patterns:
        p = re.compile(pattern, re.I)
        g = p.findall(filename)
        if len(g) > 0:
            season = g[0][0]
            season = int(re.sub("^0+", "", season))
            return season

    p = re.compile(pattern2, re.I)
    g = p.findall(filename)
    if (len(g) > 0):
        season = g[0][0] + g[0][1]
        season = int(re.sub("^0+", "", season))
        return season

    p = re.compile(pattern3, re.I)
    g = p.findall(filename)
    if (len(g) > 0):
        season = g[0][0]
        season = int(re.sub("^0+", "", season))
        return season

    return None

def handleDirectory(directory):
    memo = []
    for f in os.listdir(directory):
        f = os.path.join(directory, f)
        if os.path.isdir(f):
            handleDirectory(f)
        else:
            (root, ext) = os.path.splitext(f)
            if ext in videoTypes:
                memo.append(handleFile(f))

    return memo

def handleFile(orphanFile):
    (fpath, fname) = os.path.split(orphanFile)

    candidates = []

    if os.path.isdir(orphanFile):
        logger.error('STOP! Source is a directory and cannot be automaticly sorted!')
        return None

    for location in showLocations:
        candidates.extend(adoptionCandidates(location, orphanFile))

    def sort_func(da_sa, db_sb):
        da, sa = da_sa
        db, sb = db_sb
        return sb - sa

    candidates.sort(sort_func)

    if len(candidates) <= 0:
        return None

    # Determine Season and Episode number
    season = getSeasonNumber(fname)
    if not season:
        logger.error('\033[91m >> Move stopped. Season could not be determined. (%s) \033[0m' % str(fname))
        return None

    finaldir = os.path.join(candidates[0][0], 'Season %s' % str(season))

    # Check if season folder is present
    if not os.path.isdir(finaldir):
        os.mkdir(finaldir)

    if not os.path.isfile(os.path.join(finaldir, fname)):
        shutil.move(orphanFile, finaldir)
        logger.info('\033[92mMoved \033[95m%s\033[92m to \033[93m%s\033[0m' % (fname, finaldir))
        return fname


def sort(dir):
    return {
        'moved': filter(None, handleDirectory(dir))
    }