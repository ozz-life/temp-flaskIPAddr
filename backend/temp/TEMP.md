Определить физические устройства можно по devices/pci

```bash
ls -l /sys/class/net/
```
```bash
итого 0
lrwxrwxrwx 1 root root 0 мар 22 15:11 br-d4106a1a911e -> ../../devices/virtual/net/br-d4106a1a911e
lrwxrwxrwx 1 root root 0 мар 22 15:11 docker0 -> ../../devices/virtual/net/docker0
lrwxrwxrwx 1 root root 0 мар 22 15:11 enp5s0 -> ../../devices/pci0000:00/0000:00:01.3/0000:02:00.2/0000:03:02.0/0000:05:00.0/net/enp5s0
lrwxrwxrwx 1 root root 0 мар 22 15:11 lo -> ../../devices/virtual/net/lo
```

Выцепить непосредственно физический интерфейс. К сожалению нет вообще никаких гарантий, что на других тестовых данных и материнских платах подобное будет работать.

```bash
find /sys/class/net -mindepth 1 -maxdepth 1 -lname '*virtual*' -prune -o -printf '%f\n'
```
```bash
enp5s0
```

После отключения интерфейса и включения его заново, теряется маршрут до роутера. Перед выключением его надо куда-то сохранить, чтобы добавить вновь, чтобы не остаться без интернета. Выглядит как тот ещё костыль.

```bash
ip route
```
```bash
default via 192.168.83.0 dev enp5s0
sudo ip link set enp5s0 down
sudo ip link set enp5s0 up
sudo ip route add default via 192.168.83.0
```