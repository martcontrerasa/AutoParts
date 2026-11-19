from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal

from .models import (
    Producto,
    Carrito,
    CarritoItem,
    Pedido,
    PedidoItem,
    ClienteDistribuidor,
)


User = get_user_model()


class ProductoTests(TestCase):

    def test_producto_genera_slug_automaticamente(self):
        producto = Producto.objects.create(
            marca="Toyota",
            nombre="Filtro de Aceite",
            precio=10000
        )

        self.assertEqual(producto.slug, "filtro-de-aceite")

    def test_producto_calcula_precio_mayorista(self):
        producto = Producto.objects.create(
            marca="Toyota",
            nombre="Bujia",
            precio=10000
        )

        self.assertEqual(producto.precio_mayorista, 7500)


class CarritoTests(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username="usuario_prueba",
            password="Prueba123!"
        )

        self.producto1 = Producto.objects.create(
            marca="Toyota",
            nombre="Filtro",
            precio=10000
        )

        self.producto2 = Producto.objects.create(
            marca="Nissan",
            nombre="Bujia",
            precio=5000
        )

        self.carrito = Carrito.objects.create(
            usuario=self.usuario
        )

    def test_subtotal_de_producto_en_carrito(self):
        item = CarritoItem.objects.create(
            carrito=self.carrito,
            producto=self.producto1,
            cantidad=2
        )

        self.assertEqual(item.subtotal(), 20000)

    def test_total_del_carrito(self):
        CarritoItem.objects.create(
            carrito=self.carrito,
            producto=self.producto1,
            cantidad=2
        )

        CarritoItem.objects.create(
            carrito=self.carrito,
            producto=self.producto2,
            cantidad=3
        )

        self.assertEqual(self.carrito.total(), 35000)


class PedidoTests(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username="cliente_prueba",
            password="Prueba123!"
        )

        self.producto = Producto.objects.create(
            marca="Hyundai",
            nombre="Pastillas de Freno",
            precio=20000
        )

    def test_pedido_tiene_estado_pendiente_por_defecto(self):
        pedido = Pedido.objects.create(
            usuario=self.usuario
        )

        self.assertEqual(pedido.estado, "pendiente")
        self.assertEqual(pedido.tipo, "pedido")
        self.assertEqual(pedido.total, Decimal("0"))

    def test_pedido_item_guarda_precio_unitario(self):
        pedido = Pedido.objects.create(
            usuario=self.usuario
        )

        item = PedidoItem.objects.create(
            pedido=pedido,
            producto=self.producto,
            cantidad=2,
            precio_unitario=Decimal("20000.00")
        )

        self.assertEqual(item.cantidad, 2)
        self.assertEqual(item.precio_unitario, Decimal("20000.00"))


class ClienteDistribuidorTests(TestCase):

    def test_cliente_se_crea_activo_por_defecto(self):
        cliente = ClienteDistribuidor.objects.create(
            nombre="Cliente de Prueba"
        )

        self.assertEqual(cliente.tipo, "cliente")
        self.assertTrue(cliente.activo)
