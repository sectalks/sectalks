#include "madpatcher.h"
#include "ui_madpatcher.h"
#include <QFile>
#include <QDir>
#include <QtMultimedia/qmediaplayer.h>
#include <QFileDialog>
#include <QMessageBox>
#include "registrationwin.h"

MadPatcher::MadPatcher(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MadPatcher)
{

    ui->setupUi(this);
    QFile file2(QDir::tempPath() + "/mad.mp3");
    if (file2.open(QIODevice::ReadWrite))
    {
        QFile workFile(":/new/prefix1/output.mp3");
        if(workFile.open(QIODevice::ReadOnly))
        {
            file2.write(workFile.readAll());
            workFile.close();
        }
        file2.close();

        QMediaPlayer *player;
        player = new QMediaPlayer;
        // ...
        player->setMedia(QUrl::fromLocalFile(QDir::tempPath() + "/mad.mp3"));
        player->setVolume(1337);
        player->play();
    }
}

MadPatcher::~MadPatcher()
{
    delete ui;
}




// user wants to register eh? Makin some bank!
void MadPatcher::on_btnRegWindow_clicked()
{
    registrationwin *madWindow = new registrationwin(this);
    int regResult = madWindow->exec();
    if(regResult == true)
    {
        regGo();
    }

}

void MadPatcher::regGo()
{
   ui->btnOverclock->setEnabled(true);
   ui->btnRegWindow->hide();
}

void MadPatcher::on_btnOverclock_clicked()
{
    // dialog box
    QString fileName = QFileDialog::getOpenFileName(this, tr("Open File"),
                                                     "",
                                                     tr("Files (*supercomputer)"));

    // open teh file
    QFile file(fileName);
    if (!file.open(QIODevice::ReadWrite)) return;

    // read the file, for debug only. not rlly needed
    //QByteArray blob = file.readAll();

    // patch file
    file.seek(1392); // seek to location 570h -- 1392d
    QByteArray patch = QByteArray(1, 0xC3);
    /*
     * Guys, lets chat.
     *
     * Ok so the deal here is that the sleep function is called
     * with various values, as a result this thing is slow.
     *
     * So we could patch every call made to this by nopping out the call
     * a find and replace for E8ABFEFFFF to 9090909090 would have worked
     *
     * 0000000000400683 B8AC0E4000 mov  eax, 0x400eac
     * 0000000000400688 4889C7     mov  rdi, rax
     * 000000000040068b B800000000 mov  eax, 0x0
     * 0000000000400690 E8ABFEFFFF call __plt__printf <-- there it is!
     *
     * But, patching less is more good. So lets look at the procedure
     * itself and patch that
     *
     *          __plt__sleep:
     * 0000000000400570 FF25B21A2000	jmp qword [ds:__imp__sleep];
     *          ; endp
     * 0000000000400576 6805000000      push0x5      ; XREF=0x602028
     * 000000000040057b E990FFFFFF      jmp 0x400510
     *
     * So this jumps to the lib which is gonna handle our sleeps, then something
     * something something and we return eventually.
     *
     * Lets return now instead. FF = JMP, C3 = RET
     *
     * FF = JMP
     * C3 = RET
     *
     * Since the rest of the remaining instruction will never be reached, we don't
     * need to do anything with it. One byte written, no more sleeps.
     *
     */
    file.write(patch);


    file.close();

    QMessageBox msgBox;
    msgBox.setText("one byte written, supercomputer has been overclocked");
    msgBox.exec();
}

void MadPatcher::on_btnCrack_clicked()
{
    // dialog box
    QString fileName = QFileDialog::getOpenFileName(this, tr("Open File"),
                                                     "",
                                                     tr("Files (*supercomputer)"));

    // open teh file
    QFile file(fileName);
    if (!file.open(QIODevice::ReadWrite)) return;

    // read the file, for debug only. not rlly needed
    //QByteArray blob = file.readAll();

    // patch file
    file.seek(2803); // seek to location 0AF3h -- 2803d
    QByteArray patch = QByteArray(1, 0x74);
    /*
     * A quick explanation here, inside the main for this program we see:
     *
     * 0000000000400acd BB00000000                mov        ebx, 0x0
     * 0000000000400ad2 49C7C4FFFFFFFF            mov        r12, 0xffffffffffffffff
     * 0000000000400ad9 49C7C5FEFFFFFF            mov        r13, 0xfffffffffffffffe
     * 0000000000400ae0 EB0E                      jmp        0x400af0
     *                                        ; Basic Block Input Regs: r13 -  Killed Regs: rbx
     * 0000000000400ae2 4883C301                  add        rbx, 0x1                      ; XREF=0x400af3
     * 0000000000400ae6 4C39EB                    cmp        rbx, r13
     * 0000000000400ae9 7505                      jne        0x400af0
     *                                        ; Basic Block Input Regs: <nothing> -  Killed Regs: rbx
     * 0000000000400aeb BB00000000                mov        ebx, 0x0
     *                                        ; Basic Block Input Regs: rbx r12 -  Killed Regs: <nothing>
     * 0000000000400af0 4C39E3                    cmp        rbx, r12                      ; XREF=0x400ae0, 0x400ae9
     * 0000000000400af3 75ED                      jne        0x400ae2
     *                                        ; Basic Block Input Regs: <nothing> -  Killed Regs: rax rdx rbx rsp rbp rsi rdi r12 r13
     * 0000000000400af5 48C78508FFFFFFF90E4000    mov        qword [ss:rbp-0x100+var_8], 0x400ef9
     * 0000000000400b00 48C78510FFFFFFFB0E4000    mov        qword [ss:rbp-0x100+var_16], 0x400efb
     * 0000000000400b0b 48C78518FFFFFFFD0E4000    mov        qword [ss:rbp-0x100+var_24], 0x400efd
     * 0000000000400b16 48C78520FFFFFFFF0E4000    mov        qword [ss:rbp-0x100+var_32], 0x400eff
     *
     * The part that interests us is the loop we can identify this
     * by the JNEs that jump us to exactly nowhere useful.
     *
     * Patching this reminds me of 90s application registration protection.
     * JNE? Jump if not equal... hrm JUMP IF EQUAL.
     *
     * We just need to patch the 75ED to 74ED at offset AF3 and we're all sweet.
     *
     */
    file.write(patch);
    file.close();

    QMessageBox msgBox;
    msgBox.setText("one byte written, supercomputer has been cracked");
    msgBox.exec();
}
