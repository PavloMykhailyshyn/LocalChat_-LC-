#ifndef CMESSAGESCONTAINER_H
#define CMESSAGESCONTAINER_H

#include <QString>
#include <QPair>
#include <QVector>

typedef QVector<QPair<QString, QString>> Container;

class CMessagesContainer
{
public:
    CMessagesContainer()                            = default;
    CMessagesContainer(const CMessagesContainer&)   = default;
    ~CMessagesContainer()                           = default;

    void AddMessages(const QString& userName, const QString& message);
    void ClearContainer();
    const Container &GetContainer() const;
    int GetSize() const;

private:
    Container m_messagesContainer;
};

#endif // CMESSAGESCONTAINER_H
