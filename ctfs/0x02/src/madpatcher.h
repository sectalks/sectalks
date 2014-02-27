#ifndef MADPATCHER_H
#define MADPATCHER_H

#include <QMainWindow>

namespace Ui {
class MadPatcher;
}

class MadPatcher : public QMainWindow
{
    Q_OBJECT

public:
    explicit MadPatcher(QWidget *parent = 0);
    void regGo();
    ~MadPatcher();

private slots:

    void on_btnRegWindow_clicked();

    void on_btnCrack_clicked();

    void on_btnOverclock_clicked();

private:
    Ui::MadPatcher *ui;
};

#endif // MADPATCHER_H
