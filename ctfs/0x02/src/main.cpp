#include "madpatcher.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MadPatcher w;
    w.show();

    return a.exec();
}
