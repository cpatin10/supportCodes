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
  SimpleSemaphore llamarSupernum("/llamarSupernum", 0);
  SimpleSemaphore todosLosProductos("/todosLosProductosSem", 0);
  SimpleSemaphore mutex("/mutex", 1);
  SharedMemory<int> sm1("/mem1");
  int &clientes = sm1();
  bool atenderCaja = false;

  while(true) {
    cout << "Responder inquietudes y organizar estanterías" << endl;
    llamarSupernum.Wait();
    do {
      clienteEsperando.Wait();
      atenderCliente.Signal();
      cout << "Atendiendo cliente" << endl;
      todosLosProductos.Wait();      
      mutex.Wait();
      atenderCaja = (clientes != 0);
      mutex.Signal();
    }while(atenderCaja);
  }
}
