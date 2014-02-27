#-------------------------------------------------
#
# Project created by QtCreator 2013-12-06T18:48:34
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = MadPatcher
TEMPLATE = app
ICON = madpatcher.icns
QT += multimedia

CONFIG += mobility
MOBILITY += multimedia

#QMAKE_CXXFLAGS_RELEASE -= -O2
#QMAKE_CXXFLAGS_RELEASE += -O3

QMAKE_LFLAGS_RELEASE += -O1


SOURCES += main.cpp\
        madpatcher.cpp \
    registrationwin.cpp

HEADERS  += madpatcher.h \
    registrationwin.h

FORMS    += madpatcher.ui \
    registrationwin.ui

OTHER_FILES +=

RESOURCES += \
    Media.qrc
