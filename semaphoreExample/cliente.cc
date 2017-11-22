#ifndef __SIMPLESEMAPHORE_H_
#include "SimpleSemaphore.h"
#define __SIMPLESEMAPHORE_H_
#endif

#ifndef __SHAREDMEMORY_H_
#include "SharedMemory.h"
#define __SHAREDMEMORY_H_
#endif

#ifndef __IOSTREAM__
#include <iostream>
#define __IOSTREAM__
#endif


int main() {
  SimpleSemaphore clienteEsperando("/clienteEsperando", 0);
  SimpleSemaphore atenderCliente("/atenderCliente", 0);
  SimpleSemaphore todosLosProductos("/todosLosProductosSem", 0);
  SimpleSemaphore mutex("/mutex", 1);
  SharedMemory<int> sm1("/mem1");
  int &clientes = sm1();

  cout << "Llego cliente" << endl;
  mutex.Wait();
  ++clientes;
  mutex.Signal();
  clienteEsperando.Signal();
  atenderCliente.Wait();
  //el cliente sale de la fila y pasa a ser atendido cuando recibe la señal de quien lo vaya a atender
  mutex.Wait();
  --clientes;
  mutex.Signal();
  cout << "Pasando productos" << endl;
  sleep(3); //para hacer pruebas  
  todosLosProductos.Signal();
  cout << "Pagar y salir" << endl;

}
