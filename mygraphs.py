import basicgraphs

class graph(basicgraphs.graph):
	def deledge(self,edge):
		if edge in self._E:
			edge.head().dec_deg()
			edge.head().del_nb(edge.tail())
			edge.tail().dec_deg()
			edge.tail().del_nb(edge.head())
			index=self._E.index(edge)
			del self._E[index]
			
	def delvert(self,vertex):
		if vertex._graph==self:
			for edge in vertex.inclist():
				self.deledge(edge)
			index=self._V.index(vertex)
			del self._V[index]
				
