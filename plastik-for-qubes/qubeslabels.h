#ifndef QUBES_LABELS_H
#define QUBES_LABELS_H

class QubesLabel {
public:
    QubesLabel () {
        index = 0;
        name = "";

    }
    QubesLabel(int _index, const QString& _name, const QColor& _color, const QColor& active_text = Qt::white, const QColor& inactive_text = Qt::gray) :
        name (_name), color (_color), color_text_active (active_text), color_text_inactive (inactive_text)  {
            index = _index;
        };

    int index;
    QString name;
    QColor color, color_text_active, color_text_inactive;
};

extern QubesLabel QubesLabels[];

#define QUBES_LABEL_DOM0 0
#define QUBES_LABEL_RED 1
#define QUBES_LABEL_ORANGE 2
#define QUBES_LABEL_YELLOW 3
#define QUBES_LABEL_GREEN 4
#define QUBES_LABEL_GRAY 5
#define QUBES_LABEL_BLUE 6
#define QUBES_LABEL_PURPLE 7
#define QUBES_LABEL_BLACK 8

#define MAX_QUBES_LABELS 9

#endif
