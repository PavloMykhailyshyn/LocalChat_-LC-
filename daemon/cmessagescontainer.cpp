#include "cmessagescontainer.h"

void CMessagesContainer::AddMessages(const QString &userName, const QString &message)
{
    m_messagesContainer.push_back(qMakePair(userName, message));
}

void CMessagesContainer::ClearContainer()
{
    m_messagesContainer.clear();
}

const Container &CMessagesContainer::GetContainer() const
{
    return m_messagesContainer;
}

int CMessagesContainer::GetSize() const
{
    return m_messagesContainer.count();
}
