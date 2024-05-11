import http from 'k6/http';
import { check,sleep } from 'k6';

// Arrays de nombres y apellidos aleatorios
// const names = ['John', 'Jane', 'Michael', 'Emma', 'Chris'];
// const lastNames = ['Doe', 'Smith', 'Johnson', 'Brown', 'Taylor'];

const names = [
  'Johnan', 'Janems', 'Michaell', 'Emmy', 'Christhian', 
  'Oliver', 'Wilman', 'Ana', 'James', 'Sofia', 
  'Benjamine', 'Isabella', 'Elias', 'Mhia', 'Luca', 
  'Charlott', 'Alexandre', 'Amelis', 'Henrry', 'Evelyna'
];

const lastNames = [
  'Doeh', 'Smitha', 'Johnsona', 'Browns', 'Taylora', 
  'Williams', 'Jones', 'Garciaa', 'Millera', 'Davisa', 
  'Rodrigueza', 'Martinez', 'Hernandes', 'Lopes', 'Gonzales', 
  'Wilsona', 'Andersona', 'Thomasi', 'Moorea', 'Jacksom'
];


// Función para generar una edad aleatoria entre 18 y 60 años
function getRandomAge() {
    return Math.floor(Math.random() * (60 - 18 + 1)) + 18;
}

// Función para generar un correo electrónico único
function generateUniqueEmail() {
    const domain = 'gmail.com';
    const randomString = Math.random().toString(36).substring(2, 8);
    return `user_${randomString}@${domain}`;
}

export const options = {
    // vus: 10,
    // duration: '30s',
    stages: [
        { duration: '30s', target: 70 },
        { duration: '35s', target: 100 },
        { duration: '30s', target: 46 },
        { duration: '30s', target: 100 },
        { duration: '15s', target: 90 }
    ],
    cloud: {
        projectID: "id",
        name: 'Test (11/05/2024-14:32:27)',
    },
};

export default function () {
    // Generar datos aleatorios para el nuevo usuario
    const name = names[Math.floor(Math.random() * names.length)];
    const lastName = lastNames[Math.floor(Math.random() * lastNames.length)];
    const age = getRandomAge();
    const email = generateUniqueEmail();

    // Construir el objeto de usuario
    const newUser = {
        name: name,
        apellido: lastName,
        correo: email
    };

    // Realizar la solicitud POST para agregar el nuevo usuario
    const url = 'http://10.20.5.51:10000/';
    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    const payload = JSON.stringify(newUser);
    const res = http.post(url, payload, params);

    // Verificar la respuesta
    check(res, {
        'status is 200': (r) => r.status === 200,
        'transaction time is OK': (r) => r.timings.duration < 2000,
    });

    // Realizar una solicitud GET adicional como en tu prueba original
    http.get('http://10.20.5.51:10000/');
    http.get(`http://10.20.5.51:10000/${age}`);

    sleep(2);
}
