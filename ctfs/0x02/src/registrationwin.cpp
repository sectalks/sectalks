#include "registrationwin.h"
#include "ui_registrationwin.h"
#include <QMessageBox>

registrationwin::registrationwin(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::registrationwin)
{
    ui->setupUi(this);
    //connect(btnReg, SIGNAL(clicked), registrationwin, SLOT(regGo()));
}

registrationwin::~registrationwin()
{
    delete ui;
}

void registrationwin::on_btnCancel_clicked()
{
    reject();
}

void registrationwin::on_btnReg_clicked()
{
    // grab whatever the user has typed in
    QByteArray name = ui->txtName->text().toUtf8();
    QByteArray serial = ui->txtSerial->text().toUtf8();


    // grab first 15 chars, or pad to 15
    QByteArray stage1Serial = name.leftJustified(15, name.at(0), true);

    // this is the key we will XOR against the padded name to produce serial
    QByteArray sekritKey = "XueMmJU6)+T?ZnF";

    // perform XOR
    QByteArray stage2Serial = "";
    for(int i = 0; i < stage1Serial.length(); i++)
    {
        stage2Serial += sekritKey.at(i) ^ stage1Serial.at(i % stage1Serial.length());
    }

    // yeah its insecure, write an exploit for the crackme >_>
    //qDebug("Name: " + name);
    //qDebug("Provided Serial: " + serial);
    //qDebug("Valid Serial: " + stage2Serial.toHex());


    // is the key valid?
    bool result = strcmp(serial, stage2Serial.toHex());
    if(!result)
    {
        QMessageBox msgBox;
        msgBox.setText("Registration succesful!");
        msgBox.exec();
        accept();
    } else {
        QMessageBox msgBox;
        msgBox.setText("Nope, go away.");
        msgBox.exec();
    }
}

