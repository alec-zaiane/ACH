#!/usr/bin/env python3

import asyncio
import logging
import argparse

import WebUI
import HyperDeck


async def main(loop, args):
	hyperdeck = HyperDeck.HyperDeck(args.address, 9993)
	await hyperdeck.connect()

	webui = WebUI.WebUI()
	await webui.start(hyperdeck)


if __name__ == "__main__":
	logging.basicConfig(format='%(name)s %(levelname)s: %(message)s', level=logging.INFO)

	# Configure log level for the various modules.
	loggers = {
		'WebUI': logging.INFO,
		'HyperDeck': logging.INFO,
		'aiohttp': logging.ERROR,
	}
	for name, level in loggers.items():
		logger = logging.getLogger(name)
		logger.setLevel(level)

	# Parse command line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("address", type=str, help="IP address of the HyperDeck to connect to")
	args = parser.parse_args()

	# Run the application with the user arguments
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main(loop, args))
	loop.run_forever()
