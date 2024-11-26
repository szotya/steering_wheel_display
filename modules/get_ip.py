import socket
from modules.logger import Logger

def get_current_ip(fallback="127.0.0.1"):
	logger = Logger("get_current_ip")
	instance = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		# nem szükséges elérhető címnek lennie.
		instance.connect(("8.8.8.8", 1))
		
		ip = instance.getsockname()[0]
		logger.debug(f"Jelenlegi IP cím: {ip}")

		return ip
	except socket.error:
		logger.error(f"Hiba az IP cím meghatározásakor. Alapértelmezett IP cím ({fallback}) használva")
		return fallback;
	finally:
		instance.close()