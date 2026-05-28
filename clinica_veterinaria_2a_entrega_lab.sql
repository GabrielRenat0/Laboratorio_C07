-- =====================================================================
-- Projeto de Banco de Dados - C07 - Segunda Entrega
-- Tema: Sistema de Gerenciamento de Clinica Veterinaria
-- Integrantes:
--   Ariani Matos Trigueiro            - GES-564
--   Fabio Henrique de Sousa C. Campos - GES-389
--   Gabriel Renato de Oliveira Lopes  - GES-391
-- =====================================================================

DROP DATABASE IF EXISTS clinica_veterinaria;
CREATE DATABASE clinica_veterinaria
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE clinica_veterinaria;

CREATE TABLE dono (
    id_dono   INT AUTO_INCREMENT PRIMARY KEY,
    nome      VARCHAR(100) NOT NULL,
    cpf       CHAR(11)     NOT NULL UNIQUE,
    telefone  VARCHAR(20),
    email     VARCHAR(100)
);

CREATE TABLE veterinario (
    id_veterinario  INT AUTO_INCREMENT PRIMARY KEY,
    nome            VARCHAR(100)   NOT NULL,
    crmv            CHAR(10)       NOT NULL UNIQUE,  -- numero do conselho
    especialidade   VARCHAR(50),
    salario         DECIMAL(10, 2) NOT NULL
);

CREATE TABLE animal (
    id_animal         INT AUTO_INCREMENT PRIMARY KEY,
    nome              VARCHAR(50) NOT NULL,
    especie           ENUM('Cachorro', 'Gato', 'Ave', 'Reptil', 'Outro') NOT NULL,
    raca              VARCHAR(50),
    data_nascimento   DATE,
    peso              DOUBLE,
    possui_cadastro   BOOLEAN DEFAULT FALSE,
    observacoes       TEXT,
    id_dono           INT NOT NULL,
    CONSTRAINT fk_animal_dono FOREIGN KEY (id_dono)
        REFERENCES dono (id_dono)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE prontuario (
    id_prontuario      INT AUTO_INCREMENT PRIMARY KEY,
    alergias           TEXT,
    vacinas_em_dia     BOOLEAN DEFAULT FALSE,
    data_ultima_vacina DATE,
    id_animal          INT NOT NULL UNIQUE,
    CONSTRAINT fk_prontuario_animal FOREIGN KEY (id_animal)
        REFERENCES animal (id_animal)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE servico (
    id_servico       INT AUTO_INCREMENT PRIMARY KEY,
    nome             VARCHAR(80)     NOT NULL,
    descricao        TEXT,
    preco            DECIMAL(10, 2)  NOT NULL,
    duracao_minutos  INT             NOT NULL,
    disponivel       BOOLEAN DEFAULT TRUE,
    id_veterinario   INT             NOT NULL,
    CONSTRAINT fk_servico_vet FOREIGN KEY (id_veterinario)
        REFERENCES veterinario (id_veterinario)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE consulta (
    id_consulta     INT AUTO_INCREMENT PRIMARY KEY,
    id_animal       INT   NOT NULL,
    id_veterinario  INT   NOT NULL,
    data_consulta   DATE  NOT NULL,
    horario         TIME  NOT NULL,
    valor           FLOAT NOT NULL,
    diagnostico     TEXT,
    CONSTRAINT fk_consulta_animal FOREIGN KEY (id_animal)
        REFERENCES animal (id_animal)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_consulta_vet FOREIGN KEY (id_veterinario)
        REFERENCES veterinario (id_veterinario)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

INSERT INTO dono (nome, cpf, telefone, email) VALUES
    ('Ana Souza',         '12345678901', '(35) 99911-1111', 'ana.souza@email.com'),
    ('Carlos Mendes',     '23456789012', '(35) 99922-2222', 'carlos.m@email.com'),
    ('Mariana Lima',      '34567890123', '(35) 99933-3333', 'mari.lima@email.com'),
    ('Joao Pedro Alves',  '45678901234', '(35) 99944-4444', 'jp.alves@email.com'),
    ('Beatriz Ferreira',  '56789012345', '(35) 99955-5555', 'bia.fer@email.com');

INSERT INTO veterinario (nome, crmv, especialidade, salario) VALUES
    ('Dr. Ricardo Nunes',   'CRMV12345', 'Clinica Geral',  6500.00),
    ('Dra. Patricia Lopes', 'CRMV23456', 'Cirurgia',       8200.00),
    ('Dr. Felipe Costa',    'CRMV34567', 'Dermatologia',   7000.00),
    ('Dra. Juliana Reis',   'CRMV45678', 'Odontologia',    7500.00),
    ('Dr. Marcos Andrade',  'CRMV56789', 'Cardiologia',    9000.00);

INSERT INTO animal (nome, especie, raca, data_nascimento, peso, possui_cadastro, observacoes, id_dono) VALUES
    ('Rex',      'Cachorro', 'Labrador',         '2020-05-10', 28.5, TRUE,  'Animal docil',                  1),
    ('Mimi',     'Gato',     'Siames',           '2021-08-22',  4.2, TRUE,  'Castrada',                       2),
    ('Thor',     'Cachorro', 'Pastor Alemao',    '2019-03-15', 35.0, TRUE,  'Alergico a frango',              3),
    ('Lulu',     'Cachorro', 'Poodle',           '2022-11-01',  6.8, FALSE, 'Primeira consulta',              4),
    ('Verdinho', 'Ave',      'Periquito',        '2023-01-20',  0.1, TRUE,  'Vive em gaiola',                 5),
    ('Pingo',    'Gato',     'SRD',              '2020-07-07',  5.0, TRUE,  'Resgatado da rua',               1);

INSERT INTO prontuario (alergias, vacinas_em_dia, data_ultima_vacina, id_animal) VALUES
    ('Nenhuma',                        TRUE,  '2025-09-15', 1),
    ('Nenhuma',                        TRUE,  '2025-10-02', 2),
    ('Alergico a proteina de frango',  TRUE,  '2025-08-30', 3),
    ('Nenhuma',                        FALSE, NULL,         4),
    ('Nenhuma',                        TRUE,  '2025-11-10', 5);

INSERT INTO servico (nome, descricao, preco, duracao_minutos, disponivel, id_veterinario) VALUES
    ('Consulta de rotina',     'Avaliacao clinica geral do animal',     120.00, 30, TRUE,  1),
    ('Cirurgia de castracao',  'Procedimento cirurgico de castracao',   600.00, 90, TRUE,  2),
    ('Banho terapeutico',      'Banho com produtos dermatologicos',      80.00, 45, TRUE,  3),
    ('Limpeza dentaria',       'Profilaxia odontologica com anestesia', 350.00, 60, TRUE,  4),
    ('Eletrocardiograma',      'Exame cardiologico para diagnostico',   200.00, 40, FALSE, 5);

INSERT INTO consulta (id_animal, id_veterinario, data_consulta, horario, valor, diagnostico) VALUES
    (1, 1, '2025-11-05', '09:00:00', 120.00, 'Saudavel, vacinas em dia'),
    (2, 3, '2025-11-06', '10:30:00', 150.00, 'Dermatite leve, prescrito shampoo'),
    (3, 5, '2025-11-07', '14:00:00', 200.00, 'Sopro cardiaco grau 1, acompanhar'),
    (4, 1, '2025-11-08', '15:30:00', 120.00, 'Primeira consulta, animal saudavel'),
    (5, 1, '2025-11-09', '11:00:00', 100.00, 'Avaliacao geral sem alteracoes'),
    (6, 2, '2025-11-10', '16:00:00', 600.00, 'Encaminhado para castracao');

DROP USER IF EXISTS 'recepcionista'@'localhost';
DROP USER IF EXISTS 'assistente'@'localhost';
DROP ROLE IF EXISTS 'funcionario_clinica';

CREATE USER 'recepcionista'@'localhost' IDENTIFIED BY 'recep123';
CREATE USER 'assistente'@'localhost'    IDENTIFIED BY 'assist123';

CREATE ROLE 'funcionario_clinica';
GRANT SELECT ON clinica_veterinaria.* TO 'funcionario_clinica';
GRANT INSERT ON clinica_veterinaria.* TO 'funcionario_clinica';

GRANT 'funcionario_clinica' TO 'recepcionista'@'localhost';
GRANT 'funcionario_clinica' TO 'assistente'@'localhost';

SET DEFAULT ROLE 'funcionario_clinica' TO
    'recepcionista'@'localhost',
    'assistente'@'localhost';

CREATE OR REPLACE VIEW vw_consultas_detalhadas AS
SELECT
    c.id_consulta,
    a.nome           AS nome_animal,
    a.especie,
    d.nome           AS nome_dono,
    v.nome           AS nome_veterinario,
    v.especialidade,
    c.data_consulta,
    c.horario,
    c.valor,
    c.diagnostico
FROM consulta c
    INNER JOIN animal      a ON a.id_animal      = c.id_animal
    INNER JOIN dono        d ON d.id_dono        = a.id_dono
    INNER JOIN veterinario v ON v.id_veterinario = c.id_veterinario;

DELIMITER $$

CREATE PROCEDURE sp_agendar_consulta (
    IN p_id_animal      INT,
    IN p_id_veterinario INT,
    IN p_data           DATE,
    IN p_horario        TIME,
    IN p_valor          FLOAT,
    IN p_diagnostico    TEXT
)
BEGIN
    DECLARE v_qtd_animal INT;
    DECLARE v_qtd_vet    INT;

    SELECT COUNT(*) INTO v_qtd_animal
        FROM animal
        WHERE id_animal = p_id_animal;

    SELECT COUNT(*) INTO v_qtd_vet
        FROM veterinario
        WHERE id_veterinario = p_id_veterinario;

    IF v_qtd_animal = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Animal nao encontrado.';
    ELSEIF v_qtd_vet = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Veterinario nao encontrado.';
    ELSE
        INSERT INTO consulta (
            id_animal, id_veterinario, data_consulta, horario, valor, diagnostico
        ) VALUES (
            p_id_animal, p_id_veterinario, p_data, p_horario, p_valor, p_diagnostico
        );
    END IF;
END $$

DELIMITER ;


DELIMITER $$

CREATE TRIGGER tr_apos_inserir_animal
AFTER INSERT ON animal
FOR EACH ROW
BEGIN
    INSERT INTO prontuario (alergias, vacinas_em_dia, data_ultima_vacina, id_animal)
    VALUES ('Nenhuma registrada', FALSE, NULL, NEW.id_animal);
END $$

DELIMITER ;