CXXFLAGS=-std=c++11
LDFLAGS=-pthread -lrt
OBJECTS=SimpleSemaphore.h SharedMemory.h SharedMemoryException.h SimpleSemaphoreException.h
EXECUTABLES=productor consumidor cajero cliente supernumerario

all:  ${EXECUTABLES}

# Productor-Consumidor

consumidor: consumidor.o
	g++ -o $@ $^ ${LDFLAGS}

consumidor.o: consumidor.cc ${OBJECTS}

productor: productor.o
	g++ -o $@ $^ ${LDFLAGS}

productor.o: productor.cc ${OBJECTS}

#Tienda

tienda: cajero cliente supernumerario

cajero: cajero.o
	g++ -o $@ $^ ${LDFLAGS}

cajero.o: cajero.cc ${OBJECTS}

cliente: cliente.o
	g++ -o $@ $^ ${LDFLAGS}

cliente.o: cliente.cc ${OBJECTS}

supernumerario: supernumerario.o
	g++ -o $@ $^ ${LDFLAGS}

supernumerario.o: supernumerario.cc ${OBJECTS}

#Clean

clean:
	rm -f *.o *~
	rm -f ${EXECUTABLES}

#CleanDev

cleanDev: cleanDes cleanSem cleanMem

cleanDes:
	rm /dev/shm/*descriptor
cleanSem:
	rm /dev/shm/sem*
cleanMem:
	rm /dev/shm/mem*
