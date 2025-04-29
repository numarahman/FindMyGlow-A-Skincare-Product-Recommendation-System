# FindMyGlow - Skincare Product Recommender System
- April 29th 2024
- DSC 4900 - Data Science Project/Portfolio
- Belmont University
- Author: Numa Rahman

# Table of Contents
---
  * Introduction
  * Gathering and Cleaning Data
    * Dataset Description
    * Data Cleaning
  * Building out the Recommender System
      * Feature Engineering
      * Cosine Similarity
      * Filtering Mechanism
  * Database Creation
  * Website Creation Using Flask
  * Navigating Through the Website
  * Overview of Advanced Topics
  * Conclusion

## Introduction

The skincare industry can be overwhelming with so many products available on the market, so I wanted to build something that helps people cut through the noise. There are thousands of products out there all claiming different benefits, but it’s not always easy to know what’s actually right for your skin. Factors like skin type, sensitivity, ingredient preferences, and price range play a role in what works best for each person. My goal was to create a tool that helps users discover products based on their needs, using features that truly matter. 

## Gathering and Cleaning Data

### Gathering Data
I found this data from a publicly available dataset on Kaggle containing over 2,000 skincare products from Sephora. This is the link to the dataset: https://www.kaggle.com/datasets/nadyinky/sephora-products-and-skincare-reviews

Key Variable:
  * product_name: Name of product
  * brand_name: Name of brand
  * product_category: Kind of skincare product (e.g., moisturizer, cleanser, treatments, etc)
  * price: Price of product
  * ingredients: String of ingredients in product
  * highlights: What makes the product unique. Includes tags like "alcohol free", "cruelty free", "paraben free", "Hypoallergenic", etc.
  * for_dry_skin: Dummy variable for classifying if the product is good for dry skin
  * for_oily_skin: Dummy variable for classifying if the product is good for oily skin
  * for_combination_skin: Dummy variable for classifying if the product is good for combination skin
  * rating: Average rating of a product
  * love_counts: Number of people who loved the product
  * sephora_exclusive: Products only sold at Sephora

This histogram shows that moisturizers and treatments are the most common product types, with the widest price spread, indicating a high variety in both budget and premium offerings. The color coding reveals how different price tiers are represented within each product type, helping highlight which categories tend to skew affordable versus luxury.


## Data Cleaning

This dataset contained sephora products and its reviews, so I filtered the dataset to only include skincare products. Each product included attributes like name, brand, category, price, size, ingredients, highlights, Sephora exclusivity, and loves count.


Cleaning Steps:
  * Removed products with key missing details such as ingredients
    * I viewed ingredients as the most important feature to use for recommending. 
  * Filled missing values with appropriate values
    * For example, if highlights was null, I inputed "No highlights"
  * Standardized text (lowercased all ingredients, highlights, and brand names)
  * Parsed "highlights" into binary columns for dry, oily, combination
  * Converted features into appropriate data types for machine learning
  * Added a "price_range" to separate the products based on affordability


## Building out the Recommender System

On
