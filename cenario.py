#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 21:23:16 2017

@author: gabrui
"""
from IA import IA
from aviao import Jogador
from Simulador import Simulador
from motor import Camada, Ponto, Figura
import math


class Camera(Camada):

    def __init__(self, largura, altura, alvo, ymax):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.l2 = largura / 2
        self.a2 = altura / 2
        self.alvo = alvo
        self.fundosParalaxeInfinita = []
        self.posAntiga = Ponto(0, 0)
        self.ymax = ymax

    def _centraliza(self, ponto):
        self.pos.setXY(-ponto.getX() + self.l2, -ponto.getY() + self.a2)
        if self.pos.getY() < -self.ymax:
            self.pos.setY(-self.ymax)

    def _rot(self, angulo):
        self.rot.setAngulo(-angulo.getAngulo())

    def adicionaFilho(self, filho):
        super().adicionaFilho(filho)
        if isinstance(filho, FundoParalaxeInfinito):
            self.fundosParalaxeInfinita.append(filho)

    def removeFilho(self, filho):
        super().removeFilho(filho)
        if isinstance(filho, FundoParalaxeInfinito):
            self.fundosParalaxeInfinita.remove(filho)

    def ativarEscuta(self):
        for filho in self.filhos:
            if isinstance(filho, Simulador) or isinstance(filho, Jogador) or \
                    isinstance(filho, IA):
                filho.ativarEscuta()

    def atualiza(self, dt):
        super().atualiza(dt)
        self.posAntiga.setXY(self.pos.getX(), self.pos.getY())
        self._centraliza(self.alvo.pos)
        dx = self.pos.getX() - self.posAntiga.getX()
        dy = self.pos.getY() - self.posAntiga.getY()
        for fundo in self.fundosParalaxeInfinita:
            fundo.atualizaFundo(dx, dy)


class FundoParalaxeInfinito(Camada):

    def __init__(self, larguraTela, alturaTela, textura, rel, pos0=None,
                 corte=None):
        """
        Camada que instancia e gerencia um fundo de paralaxe infinito
        @param: textura string
        @param: corte Retangulo
        @param: pos0 Ponto
        @param: rel Ponto De -1 a 0, -1 fundo é estático
        """
        super().__init__()
        self.larguraTela = larguraTela
        self.alturaTela = alturaTela
        self.textura = textura
        self.rel = rel
        if pos0 is None:
            pos0 = Ponto(0, 0)
        self.pos0 = pos0
        figura = Figura(textura, corte)
        corte = figura.corte
        self.altura = alturaTela - corte.getAltura() - pos0.getY()
        self.largura = corte.getLargura()
        self.quant = int(math.ceil(self.larguraTela / self.largura))

        if rel.getX() < 1:
            self.quant += 1

        for i in range(self.quant):
            figura = Figura(textura, corte,
                            Ponto(i * self.largura + pos0.getX(), self.altura))
            self.adicionaFilho(figura)

    def atualizaFundo(self, dx, dy):
        print(self.filhos)
        for filho in self.filhos:
            delta = Ponto(self.rel.getX() * dx, self.rel.getY() * dy)
            filho.pos.soma(delta)
            if filho.retang.getDireita() + delta.getX() < 0:
                filho.pos.soma(Ponto(self.largura * self.quant, 0))
            elif filho.retang.getEsquerda() + delta.getX() > self.larguraTela:
                filho.pos.soma(Ponto(-self.largura * self.quant, 0))
