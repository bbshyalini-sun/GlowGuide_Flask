-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 30, 2026 at 04:59 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `skincare_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `category_id` int(11) NOT NULL,
  `category_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`category_id`, `category_name`) VALUES
(1, 'Cleanser'),
(2, 'Moisturizer'),
(3, 'Serum'),
(4, 'Toner'),
(5, 'Sunscreen');

-- --------------------------------------------------------

--
-- Table structure for table `ingredient`
--

CREATE TABLE `ingredient` (
  `ingredient_id` int(11) NOT NULL,
  `ingredient_name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ingredient`
--

INSERT INTO `ingredient` (`ingredient_id`, `ingredient_name`, `description`) VALUES
(1, 'Salicylic Acid', 'Exfoliates deep inside facial pores.'),
(2, 'Hyaluronic Acid', 'Draws hydration factors into dermal layers.'),
(3, 'Niacinamide', 'Regulates sebum output and counteracts texturing.'),
(4, 'Retinol', 'Accelerates surface cellular repair rates.'),
(5, 'Ceramides', 'Reconstructs defensive lipid barriers.'),
(6, 'Propylene Glycol', NULL),
(7, 'Alcohol Denat', NULL),
(8, 'Anhydroxylitol', NULL),
(9, 'Aqua (Water)', NULL),
(10, 'Butylene Glycol', NULL),
(11, 'Caprylyl Methicone', NULL),
(12, 'Cetyl Peg/Ppg-10/1 Dimethicone', NULL),
(13, 'Titanium Dioxide (Ci 77891)', NULL),
(14, 'Iron Oxides', NULL),
(15, 'Ethyl Paraben', NULL),
(16, 'Glucose', NULL),
(17, 'Glycerin', NULL),
(18, 'Magnesium Sulfate', NULL),
(19, 'Methylparaben', NULL),
(20, 'Mica', NULL),
(21, 'Morus Alba Leaf Extract', NULL),
(22, 'Panax Ginseng Root Extract', NULL),
(23, 'Panthenol', NULL),
(24, 'Pentaerythrityl Tetra-Di-T-Butyl Hydroxyhydrocinnamate', NULL),
(25, 'Phenoxyethanol', NULL),
(26, 'Tetrasodium Edta', NULL),
(27, 'Tocopherol Acetate', NULL),
(28, 'Triethoxycaprylylsilane', NULL),
(29, 'Xylitol', NULL),
(30, 'Xylitylglucoside', NULL),
(31, 'Hypochlorous Acid', NULL),
(32, 'Sodium Chloride', NULL),
(33, 'Bht', NULL),
(34, 'Caprylyl Glycol', NULL),
(35, 'Cetyl Ethylhexanoate', NULL),
(36, 'Glyceryl Laurate', NULL),
(37, 'Peg-12 Diisostearate', NULL),
(38, 'Peg-20 Glyceryl Triisostearate', NULL),
(39, 'Peg-8 Diisostearate', NULL),
(40, 'Polybutene', NULL),
(41, 'Ppg-15 Stearyl Ether', NULL),
(42, 'Triethylhexanoin', NULL),
(43, 'Caprylhydroxamic Acid', NULL),
(44, 'Caprylic/Capric Triglyceride', NULL),
(45, 'Caryodendron Orinocense Seed Oil', NULL),
(46, 'Cetearyl Alcohol', NULL),
(47, 'Cetearyl Olivate', NULL),
(48, 'Dicaprylyl Carbonate', NULL),
(49, 'Glyceryl Stearate', NULL),
(50, 'Limnanthes Alba (Meadowfoam) Seed Oil', NULL),
(51, 'Linoleic Acid', NULL),
(52, 'Linolenic Acid', NULL),
(53, 'Oleic Acid', NULL),
(54, 'Palmitic Acid', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `product_id` int(11) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `category_id` int(11) NOT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`product_id`, `product_name`, `category_id`, `description`) VALUES
(1, 'The Ordinary Natural Moisturising Factors + HA 30ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(2, 'CeraVe Facial Moisturising Lotion SPF 25 52ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(3, 'The Ordinary Hyaluronic Acid 2% + B5 Hydration Support Formula 30ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(4, 'AMELIORATE Transforming Body Lotion 200ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(5, 'CeraVe Moisturising Cream 454g', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(6, 'CeraVe Moisturising Lotion 473ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(7, 'CeraVe Facial Moisturising Lotion No SPF 52ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(8, 'The Ordinary Natural Moisturizing Factors + HA 100ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(9, 'CeraVe Smoothing Cream 177ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(10, 'Clinique Moisture Surge 72 Hour Moisturiser 75ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(11, 'CeraVe Moisturising Cream 50ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(12, 'CeraVe Moisturising Cream 340g', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(13, 'First Aid Beauty Ultra Repair Cream (56.7g)', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(14, 'Avène Antirougeurs Jour Redness Relief Moisturizing Protecting Cream (40ml)', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(15, 'Clinique Dramatically Different Moisturising Lotion+ 125ml with Pump', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(16, 'First Aid Beauty Ultra Repair Cream (170g)', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(17, 'Weleda Skin Food (75ml)', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(18, 'Neutrogena Hydro Boost City Shield SPF Moisturiser', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(19, 'Egyptian Magic All Purpose Skin Cream 118ml/4oz', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(20, 'JASON Aloe Vera 98% Moisturising Gel Tube 113g', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(22, 'Embryolisse Lait-Crème Concentré (75ml)', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(23, 'La Roche-Posay Effaclar H Moisturiser 40ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(24, 'Bulldog Original Moisturiser 100ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(25, 'Clinique Dramatically Different Moisturising Gel 125ml with Pump', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(26, 'La Roche-Posay Effaclar Duo+ SPF30 40ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(27, 'Avene Very High Protection B-Protect SPF 50+ 30ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(29, 'Estée Lauder DayWear Advanced Multi-Protection Anti-Oxidant Creme SPF15 N/C 50ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(33, 'La Roche-Posay Toleriane Ultra Overnight Moisturiser 40ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(35, 'Elemis Pro-Collagen Marine Cream SPF30 50ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(36, 'Avène Aqua Gel 50ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(37, 'La Roche-Posay Effaclar K(+) Anti-Blackhead Moisturiser 40ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(43, 'Estée Lauder DayWear Multi-Protection Anti-Oxidant Creme SPF 15 30ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(44, 'Elizabeth Arden Eight Hour Great 8 Daily Defense Moisturizer 45ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(45, 'Skin Doctors Sd White & Bright (50ml)', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(52, 'Clinique Moisture Surge 72 Hour Auto Replenishing Hydrator 50ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(84, 'Clinique Redness Solutions Daily Relief Cream 50ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(89, 'The INKEY List Bakuchiol Moisturiser 30ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(98, 'REN Clean Skincare Evercalm Global Protection Day Cream', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(102, 'Pai Skincare Chamomile and Rosehip Calming Day Cream 50ml', 2, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(116, 'The Ordinary 10% Agireline Solution 30ml', 3, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(117, 'The Ordinary Buffet Supersize Serum 60ml', 3, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(118, 'The Ordinary 100% Pycnogenol 5% 15ml', 3, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(119, 'Medik8 C-Tetra Serum 30ml', 3, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(120, 'Estée Lauder Advanced Night Repair Synchronized Recovery Complex II 30ml', 3, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(135, 'PIXI Collagen and Retinol Serum 30ml', 3, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(137, 'Elizabeth Arden Retinol Ceramide Capsules Line Erasing Night Serum - 30 Pieces (Sleeved Version)', 3, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(142, 'Elizabeth Arden Retinol Ceramide Capsules Line Erasing Night Serum - 60 Pieces (Sleeved Version)', 3, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(153, 'REN Clean Skincare Evercalm Anti-Redness Serum', 3, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(156, 'NIP+FAB Retinol Fix Serum Extreme 50ml', 3, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(229, 'CeraVe Hydrating Cleanser 236ml', 1, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(230, 'CeraVe Hydrating Cleanser 473ml', 1, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(231, 'The Ordinary Squalane Cleanser Supersize Exclusive 150ml', 1, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(232, 'CeraVe Foaming Facial Cleanser 473ml', 1, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(233, 'CeraVe Smoothing Cleanser 236ml', 1, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(344, 'PIXI Glow Tonic 250ml', 4, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(345, 'PIXI Retinol Tonic 100ml', 4, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(346, 'La Roche-Posay Effaclar Clarifying Lotion 200ml', 4, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(347, 'La Roche-Posay Serozinc Toner 50ml', 4, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(348, 'Caudalie Supersize Grape Water (200ml)', 4, 'Imported automated formulation. Source registry: skincare_products_clean.csv'),
(2995, 'COSRX Salicylic Acid Daily Gentle Cleanser 170g', 1, 'Imported automated formulation. Source registry: dataset'),
(2996, 'Elemis Pro-Collagen Cleansing Balm 105g', 1, 'Imported automated formulation. Source registry: dataset'),
(2997, 'FARMACY Green Clean Make Up Meltaway Cleansing Balm 100ml', 1, 'Imported automated formulation. Source registry: dataset'),
(2998, 'La Roche-Posay Effaclar H Hydrating Cleansing Cream (200ml)', 1, 'Imported automated formulation. Source registry: dataset'),
(2999, 'La Roche-Posay Effaclar Purifying Cleansing Gel 200ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3000, 'La Roche-Posay Effaclar Cleansing Gel 400ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3001, 'Emma Hardie Moringa Cleansing Balm with Professional Cleansing Cloth 100ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3002, 'Clinique Take the Day off Cleansing Balm 30ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3003, 'Clinique Liquid Facial Soap Mild 200ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3004, 'Elemis Dynamic Resurfacing Facial Wash 200ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3005, 'First Aid Beauty Face Cleanser (142g)', 1, 'Imported automated formulation. Source registry: dataset'),
(3006, 'Garnier Micellar Water Facial Cleanser and Makeup Remover for Sensitive Skin 400ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3007, 'Caudalie Duo Foaming Cleanser (2 x 150ml) (Worth £30)', 1, 'Imported automated formulation. Source registry: dataset'),
(3008, 'Liz Earle Cleanse & Polish 100ml Pump', 1, 'Imported automated formulation. Source registry: dataset'),
(3009, 'Garnier Micellar Water Facial Cleanser and Makeup Remover for Sensitive Skin 700ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3010, 'Caudalie Vinopure Purifying Gel Cleanser 150ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3011, 'Bulldog Original Face Wash 150ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3012, 'Neutrogena Hydro Boost Water Gel Cleanser 200ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3013, 'OSKIA Renaissance Cleansing Gel (100ml)', 1, 'Imported automated formulation. Source registry: dataset'),
(3014, 'NIP+FAB Teen Skin Fix Pore Blaster Night Wash 145ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3015, 'Elemis Superfood Cleansing Wash 150ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3016, 'Bioderma Hybrabio H2O 500ml Duo Pack', 1, 'Imported automated formulation. Source registry: dataset'),
(3017, 'La Roche-Posay Toleriane Dermo-Cleanser 200ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3018, 'Liz Earle Cleanse & Polish 200ml Tube', 1, 'Imported automated formulation. Source registry: dataset'),
(3019, 'Origins Checks and Balances Frothy Face Wash 150ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3020, 'Avène Cleanance Cleansing Gel 200ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3021, 'Avene Face Essentials Cleansing Foam 150ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3022, 'Clinique Anti Blemish Solutions Cleansing Foam 125ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3023, 'Neutrogena® Oil Balancing Facial Wash 200ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3024, 'Bulldog Oil Control Face Wash 150ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3025, 'Eve Lom Cleanser 200ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3026, 'REN Clean Skincare Rosa Centifolia Cleansing Gel', 1, 'Imported automated formulation. Source registry: dataset'),
(3027, 'Dr Dennis Gross Alpha Beta Pore Perfecting Cleansing Gel 60ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3028, 'La Roche-Posay Cicaplast B5 Anti-Bacterial Cleansing Wash 200ml', 1, 'Imported automated formulation. Source registry: dataset'),
(3029, 'Caudalie Instant Foaming Cleanser (150ml)', 1, 'Imported automated formulation. Source registry: dataset'),
(3030, 'CeraVe Moisturising Cream 177ml', 2, 'Imported automated formulation. Source registry: dataset'),
(3031, 'Estée Lauder Advanced Night Repair Synchronized Recovery Complex II 50ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3032, 'The Ordinary Hyaluronic Acid 2% + B5 Supersize Serum 60ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3033, 'The Ordinary Marine Hyaluronics 30ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3034, 'Avene Hydrance Intense Serum 30ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3035, 'VICHY Minéral 89 Hyaluronic Acid Hydration Booster 50ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3036, 'La Roche-Posay Pure Vitamin C10 Serum 30ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3037, 'PIXI Overnight Glow Serum', 3, 'Imported automated formulation. Source registry: dataset'),
(3038, 'Clinique Even Better Clinical Radical Dark Spot Corrector + Interrupter 50ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3039, 'Medik8 Hydr8 B5 Serum 30ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3040, 'NIP+FAB Dragons Blood Fix Serum 50ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3041, 'By Terry Cellularose CC Serum 30ml (Various Shades)', 3, 'Imported automated formulation. Source registry: dataset'),
(3042, 'NIP+FAB Salicylic Fix Serum Extreme 2% 50ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3043, 'NIOD Multi-Molecular Hyaluronic Complex 15ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3044, 'Medik8 Crystal Retinal 6', 3, 'Imported automated formulation. Source registry: dataset'),
(3045, 'Elizabeth Arden Ceramide Capsules Advanced (90 Capsules)', 3, 'Imported automated formulation. Source registry: dataset'),
(3046, 'Tan-Luxe Super Glow Body Hyaluronic Self-Tan Serum 150ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3047, 'La Roche-Posay Rosaliac AR Intense Serum 40ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3048, 'La Roche-Posay Toleriane Ultra Cream', 3, 'Imported automated formulation. Source registry: dataset'),
(3049, 'Clinique Even Better Clinical Radical Dark Spot Corrector + Interrupter 30ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3050, 'VICHY Minéral 89 Hyaluronic Acid Hydration Booster 75ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3051, 'PIXI Glow Tonic Serum 30ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3052, 'DECLÉOR Aromessence Neroli Amara Serum 15ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3053, 'The Ordinary Amino Acids + B5', 3, 'Imported automated formulation. Source registry: dataset'),
(3054, 'Lancôme Advanced Génifique Eye and Lash Serum - Light Pearl 20ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3055, 'REN Clean Skincare Radiance Perfection Serum', 3, 'Imported automated formulation. Source registry: dataset'),
(3056, 'Sanctuary Spa Hyaluronic Wonder Oil Serum 30ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3057, 'La Roche-Posay Hydraphase Intense Serum (30ml)', 3, 'Imported automated formulation. Source registry: dataset'),
(3058, 'L\'Oréal Paris Hydra Genius Liquid Care Moisturiser Combination Skin 70ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3059, 'bareMinerals SkinLongevity Vital Power Infusion Serum 50ml', 3, 'Imported automated formulation. Source registry: dataset'),
(3060, 'Elizabeth Arden Advanced Ceramide Capsules Daily Youth Restoring Eye Serum (60 Pack)', 3, 'Imported automated formulation. Source registry: dataset'),
(3061, 'Liz Earle Instant Boost Skin Tonic 200ml Bottle', 4, 'Imported automated formulation. Source registry: dataset'),
(3062, 'PIXI Retinol Tonic 250ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3063, 'PIXI Rose Tonic 100ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3064, 'Avène Gentle Toner 200ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3065, 'Natio Rosewater & Chamomile Gentle Skin Toner (250ml)', 4, 'Imported automated formulation. Source registry: dataset'),
(3066, 'Clinique Clarifying Lotion 2 200ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3067, 'Clinique Clarifying Lotion 2 400ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3068, 'PIXI Rose Tonic 250ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3069, 'Gallinée Prebiotic Face Vinegar 200ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3070, 'Sukin Hydrating Mist Toner (125ml)', 4, 'Imported automated formulation. Source registry: dataset'),
(3071, 'Caudalie Grape Water 75ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3072, 'La Roche-Posay Soothing Lotion 200ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3073, 'NIP+FAB Salicylic Fix Tonic XXL Extreme 2% 190ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3074, 'PIXI Milky Tonic 100ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3075, 'L\'Oréal Paris Fine Flowers Cleansing Toner 400ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3076, 'Estée Lauder Perfectly Clean Multi-Action Toning Lotion/Refiner 200ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3077, 'Clinique Clarifying Lotion 3 200ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3078, 'Clinique Clarifying Lotion 3 400ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3079, 'Estée Lauder Micro Essence Skin Activating Treatment Lotion Fresh with Sakura Ferment 200ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3080, 'Lancôme Tonique Confort Toner 200ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3081, 'Lancôme Tonique Confort Toner 400ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3082, 'OSKIA Floral Water Toner 30ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3083, 'First Aid Beauty Ultra Repair Wild Oat Soothing Toner 180ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3084, 'Pai Lotus and Orange Blossom BioAffinity Toner 50ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3085, 'Caudalie Moisturising Toner (100ml)', 4, 'Imported automated formulation. Source registry: dataset'),
(3086, 'Garnier Organic Thyme Toner 150ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3087, 'DECLÉOR Aroma Cleanse Essential Tonifying Lotion (200ml)', 4, 'Imported automated formulation. Source registry: dataset'),
(3088, 'NUXE Lotion Tonique Douce - Gentle Toning Lotion (200ml)', 4, 'Imported automated formulation. Source registry: dataset'),
(3089, 'REN Clean Skincare Clarimatte Clarifying Toner', 4, 'Imported automated formulation. Source registry: dataset'),
(3090, 'Sanctuary Spa Daily Glow Radiance Tonic 150ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3091, 'PIXI Milky Tonic 250ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3092, 'GLAMGLOW Supertoner 200ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3093, 'OSKIA Floral Water Toner 150ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3094, 'Neal\'s Yard Remedies Rehydrating Rose Toner 200ml', 4, 'Imported automated formulation. Source registry: dataset'),
(3095, 'Pai Skincare Rice Plant and Rosemary BioAffinity Skin Tonic 50ml', 4, 'Imported automated formulation. Source registry: dataset');

-- --------------------------------------------------------

--
-- Table structure for table `product_ingredient`
--

CREATE TABLE `product_ingredient` (
  `product_id` int(11) NOT NULL,
  `ingredient_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product_ingredient`
--

INSERT INTO `product_ingredient` (`product_id`, `ingredient_id`) VALUES
(1, 1),
(1, 2),
(2, 1),
(2, 2),
(2, 3),
(3, 2),
(3, 5),
(4, 4),
(5, 1),
(6, 2),
(7, 3),
(8, 3),
(8, 4),
(9, 1),
(9, 3),
(9, 5),
(10, 2),
(10, 3),
(11, 3),
(11, 5),
(12, 4),
(13, 2),
(16, 5),
(17, 4),
(18, 4),
(20, 1),
(20, 2),
(22, 1),
(23, 5),
(24, 4),
(26, 2),
(26, 3),
(27, 1),
(29, 2),
(33, 1),
(33, 3),
(37, 1),
(37, 2),
(84, 1),
(135, 3),
(135, 4),
(137, 4),
(142, 4),
(156, 4),
(232, 3),
(233, 1),
(233, 3),
(345, 4),
(346, 1),
(2995, 1),
(3032, 2),
(3033, 2),
(3035, 2),
(3042, 1),
(3043, 2),
(3046, 2),
(3050, 2),
(3056, 2),
(3062, 4),
(3073, 1);

-- --------------------------------------------------------

--
-- Table structure for table `product_skin_issue`
--

CREATE TABLE `product_skin_issue` (
  `product_id` int(11) NOT NULL,
  `issue_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product_skin_issue`
--

INSERT INTO `product_skin_issue` (`product_id`, `issue_id`) VALUES
(1, 7),
(2, 1),
(2, 9),
(3, 2),
(3, 8),
(4, 2),
(4, 3),
(4, 7),
(5, 8),
(6, 8),
(7, 9),
(8, 7),
(9, 1),
(9, 9),
(10, 5),
(10, 10),
(11, 8),
(12, 8),
(13, 7),
(14, 3),
(14, 4),
(15, 2),
(15, 3),
(16, 7),
(17, 2),
(18, 1),
(19, 2),
(20, 7),
(20, 8),
(22, 8),
(23, 8),
(24, 2),
(24, 3),
(25, 2),
(25, 3),
(26, 1),
(26, 9),
(27, 1),
(29, 1),
(29, 3),
(29, 10),
(33, 5),
(33, 7),
(33, 9),
(35, 1),
(35, 3),
(35, 5),
(36, 2),
(37, 1),
(43, 1),
(43, 3),
(43, 10),
(44, 1),
(44, 10),
(45, 1),
(45, 3),
(45, 5),
(52, 5),
(52, 10),
(84, 1),
(84, 3),
(84, 4),
(89, 2),
(89, 3),
(89, 6),
(98, 2),
(98, 4),
(102, 2),
(102, 4),
(116, 5),
(117, 2),
(117, 5),
(117, 7),
(117, 10),
(118, 8),
(119, 8),
(120, 3),
(120, 5),
(120, 10),
(135, 5),
(135, 6),
(135, 9),
(135, 10),
(137, 2),
(137, 5),
(137, 6),
(142, 2),
(142, 5),
(142, 6),
(153, 2),
(153, 4),
(156, 2),
(156, 5),
(156, 6),
(229, 8),
(230, 8),
(231, 8),
(232, 9),
(233, 1),
(233, 9),
(344, 2),
(344, 8),
(344, 10),
(345, 2),
(345, 5),
(345, 6),
(345, 8),
(346, 1),
(346, 2),
(347, 8),
(348, 8),
(2995, 1),
(2996, 5),
(2997, 8),
(2998, 8),
(2999, 8),
(3000, 8),
(3001, 8),
(3002, 8),
(3003, 8),
(3004, 8),
(3005, 8),
(3006, 7),
(3007, 8),
(3008, 8),
(3009, 7),
(3010, 8),
(3011, 8),
(3012, 8),
(3013, 8),
(3014, 1),
(3015, 8),
(3016, 8),
(3017, 7),
(3018, 8),
(3019, 8),
(3020, 8),
(3021, 8),
(3022, 1),
(3023, 8),
(3024, 3),
(3025, 8),
(3026, 8),
(3027, 1),
(3028, 4),
(3029, 8),
(3030, 8),
(3031, 8),
(3032, 8),
(3033, 8),
(3034, 8),
(3035, 8),
(3036, 10),
(3037, 10),
(3038, 9),
(3039, 8),
(3040, 8),
(3041, 8),
(3042, 1),
(3043, 8),
(3044, 8),
(3045, 8),
(3046, 8),
(3046, 10),
(3047, 8),
(3048, 7),
(3049, 9),
(3050, 8),
(3051, 10),
(3052, 8),
(3053, 8),
(3054, 8),
(3055, 10),
(3056, 8),
(3057, 8),
(3058, 8),
(3059, 8),
(3060, 8),
(3061, 8),
(3062, 6),
(3063, 8),
(3064, 8),
(3065, 8),
(3068, 8),
(3069, 8),
(3070, 8),
(3071, 8),
(3072, 7),
(3073, 1),
(3074, 8),
(3075, 8),
(3076, 8),
(3079, 10),
(3080, 8),
(3081, 8),
(3082, 8),
(3083, 7),
(3084, 8),
(3085, 8),
(3086, 8),
(3087, 8),
(3088, 8),
(3089, 3),
(3090, 10),
(3091, 8),
(3092, 10),
(3093, 8),
(3094, 8),
(3095, 8);

-- --------------------------------------------------------

--
-- Table structure for table `product_skin_type`
--

CREATE TABLE `product_skin_type` (
  `product_id` int(11) NOT NULL,
  `skin_type_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product_skin_type`
--

INSERT INTO `product_skin_type` (`product_id`, `skin_type_id`) VALUES
(1, 2),
(1, 4),
(2, 2),
(3, 2),
(4, 4),
(5, 2),
(6, 2),
(7, 2),
(8, 4),
(9, 1),
(9, 2),
(10, 3),
(11, 2),
(12, 2),
(13, 2),
(13, 4),
(14, 2),
(15, 2),
(16, 2),
(16, 4),
(17, 3),
(18, 3),
(19, 2),
(20, 1),
(20, 2),
(20, 4),
(22, 3),
(23, 3),
(24, 3),
(25, 1),
(25, 2),
(26, 3),
(27, 3),
(29, 3),
(33, 4),
(35, 2),
(36, 1),
(37, 1),
(43, 3),
(44, 3),
(45, 3),
(52, 3),
(84, 1),
(84, 2),
(89, 3),
(98, 2),
(102, 2),
(102, 4),
(116, 1),
(117, 4),
(118, 3),
(119, 3),
(120, 3),
(135, 3),
(137, 3),
(142, 3),
(153, 3),
(156, 3),
(229, 3),
(230, 3),
(231, 3),
(232, 1),
(233, 1),
(344, 3),
(345, 3),
(346, 1),
(347, 3),
(348, 3),
(2995, 1),
(2995, 4),
(2996, 2),
(2997, 2),
(2998, 2),
(2999, 1),
(3000, 1),
(3001, 2),
(3002, 2),
(3003, 3),
(3004, 3),
(3005, 3),
(3006, 4),
(3007, 1),
(3008, 3),
(3009, 4),
(3010, 1),
(3011, 3),
(3012, 1),
(3013, 1),
(3014, 3),
(3015, 3),
(3016, 3),
(3017, 3),
(3018, 3),
(3019, 3),
(3020, 1),
(3021, 1),
(3022, 1),
(3023, 3),
(3024, 3),
(3025, 3),
(3026, 1),
(3027, 1),
(3028, 4),
(3029, 1),
(3030, 2),
(3031, 3),
(3032, 2),
(3033, 2),
(3034, 3),
(3035, 2),
(3036, 3),
(3037, 3),
(3038, 3),
(3039, 3),
(3040, 3),
(3041, 3),
(3042, 1),
(3043, 2),
(3044, 3),
(3045, 3),
(3046, 2),
(3047, 3),
(3048, 2),
(3049, 3),
(3050, 2),
(3051, 3),
(3052, 3),
(3053, 3),
(3054, 3),
(3055, 3),
(3056, 2),
(3057, 3),
(3058, 3),
(3059, 3),
(3060, 3),
(3061, 3),
(3062, 3),
(3063, 3),
(3064, 4),
(3065, 4),
(3066, 3),
(3067, 3),
(3068, 3),
(3069, 3),
(3070, 3),
(3071, 3),
(3072, 3),
(3073, 1),
(3074, 3),
(3075, 3),
(3076, 3),
(3077, 3),
(3078, 3),
(3079, 3),
(3080, 3),
(3081, 3),
(3082, 3),
(3083, 3),
(3084, 3),
(3085, 2),
(3086, 3),
(3087, 3),
(3088, 4),
(3089, 1),
(3090, 3),
(3091, 3),
(3092, 3),
(3093, 3),
(3094, 3),
(3095, 3);

-- --------------------------------------------------------

--
-- Table structure for table `skin_issue`
--

CREATE TABLE `skin_issue` (
  `issue_id` int(11) NOT NULL,
  `issue_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `skin_issue`
--

INSERT INTO `skin_issue` (`issue_id`, `issue_name`) VALUES
(1, 'Acne'),
(2, 'Severe Dryness'),
(3, 'Excess Sebum'),
(4, 'Chronic Redness'),
(5, 'Fine Lines'),
(6, 'Deep Wrinkles'),
(7, 'Hyper-Sensitivity'),
(8, 'Acute Dehydration'),
(9, 'Dark Spots'),
(10, 'Dullness');

-- --------------------------------------------------------

--
-- Table structure for table `skin_type`
--

CREATE TABLE `skin_type` (
  `skin_type_id` int(11) NOT NULL,
  `skin_type_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `skin_type`
--

INSERT INTO `skin_type` (`skin_type_id`, `skin_type_name`) VALUES
(1, 'Oily'),
(2, 'Dry'),
(3, 'Combination'),
(4, 'Sensitive');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`category_id`);

--
-- Indexes for table `ingredient`
--
ALTER TABLE `ingredient`
  ADD PRIMARY KEY (`ingredient_id`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`product_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `product_ingredient`
--
ALTER TABLE `product_ingredient`
  ADD PRIMARY KEY (`product_id`,`ingredient_id`),
  ADD KEY `ingredient_id` (`ingredient_id`);

--
-- Indexes for table `product_skin_issue`
--
ALTER TABLE `product_skin_issue`
  ADD PRIMARY KEY (`product_id`,`issue_id`),
  ADD KEY `issue_id` (`issue_id`);

--
-- Indexes for table `product_skin_type`
--
ALTER TABLE `product_skin_type`
  ADD PRIMARY KEY (`product_id`,`skin_type_id`),
  ADD KEY `skin_type_id` (`skin_type_id`);

--
-- Indexes for table `skin_issue`
--
ALTER TABLE `skin_issue`
  ADD PRIMARY KEY (`issue_id`);

--
-- Indexes for table `skin_type`
--
ALTER TABLE `skin_type`
  ADD PRIMARY KEY (`skin_type_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `ingredient`
--
ALTER TABLE `ingredient`
  MODIFY `ingredient_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3096;

--
-- AUTO_INCREMENT for table `skin_issue`
--
ALTER TABLE `skin_issue`
  MODIFY `issue_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `skin_type`
--
ALTER TABLE `skin_type`
  MODIFY `skin_type_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `product`
--
ALTER TABLE `product`
  ADD CONSTRAINT `product_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`) ON DELETE CASCADE;

--
-- Constraints for table `product_ingredient`
--
ALTER TABLE `product_ingredient`
  ADD CONSTRAINT `product_ingredient_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `product_ingredient_ibfk_2` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredient` (`ingredient_id`) ON DELETE CASCADE;

--
-- Constraints for table `product_skin_issue`
--
ALTER TABLE `product_skin_issue`
  ADD CONSTRAINT `product_skin_issue_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `product_skin_issue_ibfk_2` FOREIGN KEY (`issue_id`) REFERENCES `skin_issue` (`issue_id`) ON DELETE CASCADE;

--
-- Constraints for table `product_skin_type`
--
ALTER TABLE `product_skin_type`
  ADD CONSTRAINT `product_skin_type_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `product_skin_type_ibfk_2` FOREIGN KEY (`skin_type_id`) REFERENCES `skin_type` (`skin_type_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
