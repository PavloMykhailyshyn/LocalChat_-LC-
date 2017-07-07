#include <QCoreApplication>
#include <QDebug>
#include <QFileInfo>

#include <iostream>

#include "cusermessagesdb.h"
#include "common_libs.h"

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);

    CUserMessagesDB db("user_messages","localhost",
                       "root", "mysqlpass");
    CMessagesContainer container;

    if (db.ConnectToBD())
    {
        db.AddMessageQuery("ololosh", "hello");
        db.AddMessageQuery("ololosh", "world");

        db.GetMessages("ololosh" ,container);
        qDebug() << "Size = " << container.GetSize();

        for (auto x : container.GetContainer())
        {
            qDebug() << x.first;
            qDebug() << x.second;
        }

        db.DeleteMessages("ololosh");
        container.ClearContainer();

        db.GetMessages("ololosh", container);

        qDebug() << "Size = " << container.GetSize();

    }
    else
    {
        qDebug() << "Can't open db! Exit failure...";
    }

    SniffInterface();

    return a.exec();
}
