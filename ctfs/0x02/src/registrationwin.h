#ifndef REGISTRATIONWIN_H
#define REGISTRATIONWIN_H

#include <QDialog>

namespace Ui {
class registrationwin;
}

class registrationwin : public QDialog
{
    Q_OBJECT

public:
    explicit registrationwin(QWidget *parent = 0);
    ~registrationwin();

private slots:
    void on_btnCancel_clicked();

    void on_btnReg_clicked();

private:
    Ui::registrationwin *ui;
};

#endif // REGISTRATIONWIN_H
