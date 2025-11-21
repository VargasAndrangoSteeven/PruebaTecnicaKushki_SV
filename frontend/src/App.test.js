/**
 * Autor: Steeven Vargas
 * Fecha: Noviembre 2024
 * Descripción: Pruebas básicas de ejemplo para demostrar Jest
 */

describe('Pruebas de Ejemplo del Sistema', () => {
  test('la suma funciona correctamente', () => {
    expect(1 + 1).toBe(2);
  });

  test('los strings se concatenan', () => {
    const saludo = 'Hola' + ' ' + 'Mundo';
    expect(saludo).toBe('Hola Mundo');
  });

  test('los arrays contienen elementos', () => {
    const numeros = [1, 2, 3, 4, 5];
    expect(numeros).toContain(3);
    expect(numeros.length).toBe(5);
  });

  test('los objetos tienen propiedades', () => {
    const usuario = {
      nombre: 'Test',
      edad: 25
    };
    expect(usuario).toHaveProperty('nombre');
    expect(usuario.nombre).toBe('Test');
  });

  test('las promesas se resuelven', async () => {
    const promesa = Promise.resolve('Éxito');
    await expect(promesa).resolves.toBe('Éxito');
  });

  test('verificación de tipos', () => {
    expect(typeof 'texto').toBe('string');
    expect(typeof 123).toBe('number');
    expect(typeof true).toBe('boolean');
  });
});
