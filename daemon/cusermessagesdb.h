#ifndef CUSERMESSAGESDB_H
#define CUSERMESSAGESDB_H

#include <QDir>
#include <QFileInfo>
#include <QString>
#include <QtSql/QSqlDatabase>
#include <QtSql/QSqlError>
#include <QtSql/QSqlQuery>

#include "cmessagescontainer.h"

const QString g_cDataBaseMySqlDriver =           "QSQLITE";
const QString g_cDBName              = "/users_messages.db";
const QString g_cTableName           =          "messages";

class CUserMessagesDB
{
public:
    CUserMessagesDB(const QString& dbName, const QString& hostName,
                    const QString& userName, const QString& pass);
    ~CUserMessagesDB();

    bool ConnectToBD();
    bool IsOpen() const;
    bool AddMessageQuery(const QString& userName, const QString& message);
    bool DeleteMessages(const QString& userName);
    void GetMessages(const QString& userName,
                              CMessagesContainer &container);

private:
    void GetLastDBError(const QString& errorMessage) const;
    void CreateDataBaseIfNotExist(const QString& db_name);
    void CreateTable(const QString& tableName);

private:
    QSqlDatabase m_dataBase;
    bool          m_bIsOpen;
};

#endif // CUSERMESSAGESDB_H
