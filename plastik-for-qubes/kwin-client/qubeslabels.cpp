#include "plastik.h"

QubesLabel QubesLabels[] = {
    QubesLabel (QUBES_LABEL_DOM0, "dom0", QColor::fromHsv (0, 0, 220), Qt::black),
    QubesLabel (QUBES_LABEL_RED, "red", QColor::fromHsv (0,200, 220)),
    QubesLabel (QUBES_LABEL_ORANGE, "orange", QColor::fromHsv (30,255, 250), Qt::black, Qt::darkGray),
    QubesLabel (QUBES_LABEL_YELLOW, "yellow", QColor::fromHsv (60,250, 220), Qt::black, Qt::darkGray),
    QubesLabel (QUBES_LABEL_GREEN, "green", QColor::fromHsv (120,250, 200), Qt::black, Qt::darkGray),
    QubesLabel (QUBES_LABEL_GRAY, "gray", QColor::fromHsv (0,0, 150), Qt::black),
    QubesLabel (QUBES_LABEL_BLUE, "blue", QColor::fromHsv (220,200, 220)),
    QubesLabel (QUBES_LABEL_PURPLE, "purple", QColor::fromHsv (300,255, 99)),
    QubesLabel (QUBES_LABEL_BLACK, "black", QColor::fromHsv (0, 0, 0))
};


