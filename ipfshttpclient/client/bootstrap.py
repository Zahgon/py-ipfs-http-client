from . import base


class Section(base.SectionBase):
	@base.returns_single_item(base.ResponseBase)
	def add(self, peer: base.multiaddr_t, *peers: base.multiaddr_t,
	        **kwargs: base.CommonArgs):
		"""Adds peers to the bootstrap list
		
		Parameters
		----------
		peer
			IPFS Multiaddr of a peer to add to the list
		
		Returns
		-------
			dict
		"""
		pass
	
	
	@base.returns_single_item(base.ResponseBase)
	def list(self, **kwargs: base.CommonArgs):
		"""Returns the addresses of peers used during initial discovery of the
		IPFS network
		
		Peers are output in the format ``<multiaddr>/<peerID>``.
		
		.. code-block:: python
		
			>>> client.bootstrap.list()
			{'Peers': [
				'/ip4/104.131.131.82/tcp/4001/ipfs/QmaCpDMGvV2BGHeYER â€¦ uvuJ',
				'/ip4/104.236.176.52/tcp/4001/ipfs/QmSoLnSGccFuZQJzRa â€¦ ca9z',
				'/ip4/104.236.179.241/tcp/4001/ipfs/QmSoLPppuBtQSGwKD â€¦ KrGM',
				â€¦
				'/ip4/178.62.61.185/tcp/4001/ipfs/QmSoLMeWqB7YGVLJN3p â€¦ QBU3'
			]}
		
		Returns
		-------
			dict
		
		+-------+-------------------------------+
		| Peers | List of known bootstrap peers |
		+-------+-------------------------------+
		"""
		pass
	
	
	@base.returns_single_item(base.ResponseBase)
	def rm(self, peer: base.multiaddr_t, *peers: base.multiaddr_t,
	       **kwargs: base.CommonArgs):
		"""Removes peers from the bootstrap list
		
		Parameters
		----------
		peer
			IPFS Multiaddr of a peer to remove from the list
		
		Returns
		-------
			dict
		"""
		pass
