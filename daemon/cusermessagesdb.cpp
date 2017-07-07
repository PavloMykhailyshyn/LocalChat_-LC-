#include "cusermessagesdb.h"
#include <QDebug>

CUserMessagesDB::CUserMessagesDB(const QString &dbName, const QString &hostName,
                                 const QString &userName, const QString &pass) : m_bIsOpen(false)
{
    m_dataBase = QSqlDatabase::addDatabase(g_cDataBaseMySqlDriver);

    QDir currenPaht;

    QString path = currenPaht.currentPath() + g_cDBName;

    m_dataBase.setDatabaseName(path);

    m_dataBase.open();

    QSqlQuery query;
    if (query.exec("create table messages "
              "(user_name char(255), "
               "message   char(255))"))
    {
        qDebug() << "all ok!";
    }
    else
    {
        qDebug() << query.lastError().text();
    }
}

CUserMessagesDB::~CUserMessagesDB()
{
    if (m_bIsOpen)
    {
        m_dataBase.close();
    }
}

bool CUserMessagesDB::ConnectToBD()
{
    if (!m_dataBase.open())
    {
        GetLastDBError(m_dataBase.lastError().text());
        m_bIsOpen = false;
    }
    else
    {
        m_bIsOpen = true;
    }

    return m_bIsOpen;
}

bool CUserMessagesDB::IsOpen() const
{
    return m_bIsOpen;
}

bool CUserMessagesDB::AddMessageQuery(const QString &userName, const QString &message)
{
    bool queryExecState = false;
    QSqlQuery sqlQuery = QSqlQuery(m_dataBase);

    QString query = QString("INSERT INTO %1 VALUES('%2', '%3');").arg(g_cTableName, userName, message);

    if (sqlQuery.exec(query))
    {
        queryExecState = true;
    }
    else
    {
        GetLastDBError(sqlQuery.lastError().text());
    }

    return queryExecState;
}

bool CUserMessagesDB::DeleteMessages(const QString &userName)
{
    bool queryExecState = false;
    QSqlQuery sqlQuery = QSqlQuery(m_dataBase);
    QString query = QString("DELETE FROM %1 WHERE user_name = '%2';").arg(
                                                       g_cTableName, userName);

    if (sqlQuery.exec(query))
    {
        queryExecState = true;
    }
    else
    {
        GetLastDBError(sqlQuery.lastError().text());
    }

    return queryExecState;
}

void CUserMessagesDB::GetMessages(const QString &userName, CMessagesContainer &container)
{
    QSqlQuery sqlQuery = QSqlQuery(m_dataBase);
    QString query = QString("SELECT * FROM %1 WHERE user_name = '%2';").arg(g_cTableName,
                                                                  userName);

    if (sqlQuery.exec(query))
    {
        while (sqlQuery.next())
        {
            container.AddMessages(sqlQuery.value(0).toString(), sqlQuery.value(1).toString());
        }
    }
    else
    {
        GetLastDBError(sqlQuery.lastError().text());
    }
}

void CUserMessagesDB::GetLastDBError(const QString &errorMessage) const
{
    qDebug() << errorMessage;
}

void CUserMessagesDB::CreateDataBaseIfNotExist(const QString &db_name)
{

}

void CUserMessagesDB::CreateTable(const QString &tableName)
{
    QSqlQuery query(m_dataBase);

    query.prepare( QString("CREATE TABLE %1(user_name CHAR(255), message(255));").arg(tableName));

    if(query.exec()){
        qDebug() << "Table created success!";
    }
    else{
        qDebug()<<"MySQL error:" + query.lastError().text();
    }
}
