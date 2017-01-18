# ifdown $1
# ifup -v $1
# sudo route del -net 0.0.0.0 dev $2
# sudo route add -host $3 netmask 255.255.255.0 gw $4 dev $2

# start to install package needed 

# echo y | sudo apt-get install rabbitmq-server
# echo y | sudo apt-get install python
# sudo pip install pika

git clone git://github.com/alanxz/rabbitmq-c.git
cd rabbitmq-c
# git checkout e1746f92585d59364fc48b6305ce25d7fc86c2a4
hg clone  http://hg.rabbitmq.com/rabbitmq-codegen/
rm -r codegen
mv rabbitmq-codegen codegen
mkdir build && cd build
cmake ..
cmake --build .
cd librabbitmq
make
make install
sudo cp ../../librabbitmq/*.h /usr/local/include
sudo cp librabbitmq.a /usr/local/lib
sudo ldconfig

git clone https://github.com/akalend/amqpcpp.git
cd amqpcpp
make
sudo cp libamqpcpp.a /usr/local/lib

# copy all the staff needed 
cd ~/Desktop
git clone https://andrew199105@bitbucket.org/andrew199105/navigation.git
mv navigation Navigation


