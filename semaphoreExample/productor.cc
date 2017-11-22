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
  SimpleSemaphore sem1("/sem-empty",1);
  SimpleSemaphore sem2("/sem-full",0);
  SharedMemory<int> sm("/mem");
  int &i = sm();
  int producto;

  //produce
  while (true){
    cout << "Produciendo" << endl;
    producto = getpid();
    sleep(3);
    cout << "Producto = " << producto << endl;
    sem1.Wait();
    i = producto;
    sem2.Signal();
    cout << "Producto entregado" << endl;
  }
        
  return 0;
}
