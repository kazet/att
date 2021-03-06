class Corpus(object):
  def GetLanguages(self):
    return self._languages

  def GetMultilingualDocument(self, identifier):
    raise NotImplementedError()

  def GetMultilingualDocumentIdentifiers(self):
    raise NotImplementedError()

  def GetFirstIdentifiers(self, num):
    return list(self.GetMultilingualDocumentIdentifiers())[:num]

  def GetMultilingualDocuments(self):
    for identifier in self.GetMultilingualDocumentIdentifiers():
      yield self.GetMultilingualDocument(identifier)

  def GetMultilingualAlignedDocuments(self):
    for identifier in self.GetMultilingualDocumentIdentifiers():
      yield self.GetMultilingualAlignedDocument(identifier)

  def GetMultilingualAlignedDocument(self, identifier):
    raise Exception("Requested aligned documents in a corpus that is not aligned")
