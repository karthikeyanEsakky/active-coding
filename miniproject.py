import rasterio
import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime



print("="*60)
print("📡 STEP 1: LOADING AND CLASSIFYING SATELLITE IMAGE")
print("="*60)


scale = 5   

with rasterio.open('T44PMV_20260307T050241_B04_10m.jp2') as red_src:
    red = red_src.read(
        1,
        out_shape=(red_src.height // scale, red_src.width // scale)
    ).astype(float)

with rasterio.open('T44PMV_20260307T050241_B08_10m.jp2') as nir_src:
    nir = nir_src.read(
        1,
        out_shape=(nir_src.height // scale, nir_src.width // scale)
    ).astype(float)


with rasterio.open('T44PMV_20260307T050241_B04_10m.jp2') as src:
    bounds = src.bounds
    image_center_lat = (bounds.top + bounds.bottom) / 2
    image_center_lon = (bounds.left + bounds.right) / 2
    print(f"📍 Image Center Coordinates: {image_center_lat:.4f}°N, {image_center_lon:.4f}°E")

try:
    with rasterio.open('T44PMV_20260307T050241_B03_10m.jp2') as green_src:
        green = green_src.read(
            1,
            out_shape=(green_src.height // scale, green_src.width // scale)
        ).astype(float)

    with rasterio.open('T44PMV_20260307T050241_B02_10m.jp2') as blue_src:
        blue = blue_src.read(
            1,
            out_shape=(blue_src.height // scale, blue_src.width // scale)
        ).astype(float)

    rgb_available = True
except:
    rgb_available = False
    print("⚠️ RGB bands not available")

print("✅ Bands loaded successfully")

if rgb_available:
    rgb = np.dstack((red, green, blue))
    rgb_norm = cv2.normalize(rgb, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Enhancement (CLAHE + Sharpen)
    lab = cv2.cvtColor(rgb_norm, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    l_enhanced = clahe.apply(l)

    enhanced_rgb = cv2.cvtColor(cv2.merge((l_enhanced, a, b)), cv2.COLOR_LAB2RGB)

    kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
    enhanced_rgb = cv2.filter2D(enhanced_rgb, -1, kernel)

    plt.figure(figsize=(10,5))
    plt.subplot(1,2,1)
    plt.imshow(rgb_norm)
    plt.title("Original RGB")
    plt.axis('off')

    plt.subplot(1,2,2)
    plt.imshow(enhanced_rgb)
    plt.title("Enhanced RGB")
    plt.axis('off')
    plt.show()

ndvi = (nir - red) / (nir + red + 1e-5)
print("✅ NDVI calculated")

X = np.stack([
    red.flatten(),
    nir.flatten(),
    ndvi.flatten()
], axis=1)

y = np.zeros(X.shape[0])
y[ndvi.flatten() > 0.3] = 1   
y[ndvi.flatten() < 0] = 0     
y[(ndvi.flatten() >= 0) & (ndvi.flatten() <= 0.3)] = 2  

model = RandomForestClassifier(n_estimators=10)
model.fit(X, y)

pred = model.predict(X)
classified = pred.reshape(red.shape)

plt.figure(figsize=(6,6))
plt.imshow(classified, cmap='jet')
plt.title("Land Classification (0=Water, 1=Vegetation, 2=Urban)")
plt.colorbar()
plt.axis('off')
plt.show()

total_pixels = classified.size
water_pct = np.sum(classified == 0) / total_pixels * 100
veg_pct = np.sum(classified == 1) / total_pixels * 100
urban_pct = np.sum(classified == 2) / total_pixels * 100

print("\n📊 LAND COVER STATISTICS:")
print(f"   💧 Water: {water_pct:.1f}%")
print(f"   🌿 Vegetation: {veg_pct:.1f}%")
print(f"   🏙️  Urban: {urban_pct:.1f}%")


print("\n" + "="*60)
print("🌱 STEP 2: SOIL IDENTIFICATION (Offline - India Soil Zones)")
print("="*60)

def get_soil_offline(latitude, longitude):
    """
    Identify soil type using India's geographical soil zones
    No API required - works completely offline
    """
    
    print(f"\n📍 Analyzing Location: {latitude}°N, {longitude}°E")
    
    if (latitude >= 23.0 and latitude <= 30.5 and 
        longitude >= 68.0 and longitude <= 76.0):
        
        soil_type = "Desert / Sandy Soil (Rajsthan Desert)"
        sand, clay, silt = 85, 5, 10
        ph = 8.3
        ph_status = "Alkaline"
        texture = "Sandy"
        region = "Thar Desert Region"
        characteristics = "Very low organic matter, excellent drainage, low fertility"
        suitable_crops = ["Millets (Bajra)", "Pulses", "Watermelon", "Cactus", "Date Palm"]
        
    elif ((latitude >= 16.0 and latitude <= 22.5 and longitude >= 72.0 and longitude <= 80.0) or
          (latitude >= 15.0 and latitude <= 18.0 and longitude >= 75.0 and longitude <= 78.0)):
        
        soil_type = "Black Cotton Soil (Regur)"
        sand, clay, silt = 25, 55, 20
        ph = 7.9
        ph_status = "Slightly Alkaline"
        texture = "Clayey"
        region = "Deccan Plateau (Black Soil Belt)"
        characteristics = "High clay content, good water retention, rich in calcium & magnesium"
        suitable_crops = ["Cotton", "Sugarcane", "Wheat", "Sorghum (Jowar)", "Soybean", "Chilli"]
        
    elif ((latitude >= 24.0 and latitude <= 31.0 and longitude >= 73.0 and longitude <= 88.0) or
          (latitude >= 21.0 and latitude <= 25.0 and longitude >= 86.0 and longitude <= 89.0)):
        
        soil_type = "Alluvial Soil"
        sand, clay, silt = 40, 22, 38
        ph = 7.3
        ph_status = "Neutral to Slightly Alkaline"
        texture = "Loamy"
        region = "Indo-Gangetic Plains"
        characteristics = "Most fertile soil, rich in potash & lime, excellent for agriculture"
        suitable_crops = ["Rice", "Wheat", "Sugarcane", "Maize", "Pulses", "Oilseeds", "Vegetables"]
        
    elif ((latitude >= 10.0 and latitude <= 20.0 and longitude >= 75.0 and longitude <= 85.0) or
          (latitude >= 20.0 and latitude <= 24.0 and longitude >= 83.0 and longitude <= 87.0)):
        
        soil_type = "Red Soil"
        sand, clay, silt = 60, 18, 22
        ph = 6.5
        ph_status = "Slightly Acidic to Neutral"
        texture = "Sandy Loam"
        region = "Peninsular Plateau (Red Soil Zone)"
        characteristics = "Rich in iron oxide, low in nitrogen & phosphorus"
        suitable_crops = ["Groundnut", "Ragi (Finger Millet)", "Tobacco", "Potato", "Fruits", "Maize"]
        
    elif ((latitude >= 8.0 and latitude <= 15.0 and longitude >= 74.0 and longitude <= 78.0) or
          (latitude >= 22.0 and latitude <= 28.0 and longitude >= 88.0 and longitude <= 97.0)):
        
        soil_type = "Laterite Soil"
        sand, clay, silt = 45, 35, 20
        ph = 5.8
        ph_status = "Acidic"
        texture = "Gravelly Clay"
        region = "Western Ghats & Northeastern Hills"
        characteristics = "High iron & aluminum, low fertility, requires heavy fertilization"
        suitable_crops = ["Tea", "Coffee", "Cashew", "Rubber", "Coconut", "Arecanut", "Pepper"]
        
    elif (latitude >= 30.0 and latitude <= 37.0 and longitude >= 72.0 and longitude <= 97.0):
        
        soil_type = "Mountain / Forest Soil"
        sand, clay, silt = 35, 28, 37
        ph = 6.2
        ph_status = "Slightly Acidic"
        texture = "Skeletal/Loamy"
        region = "Himalayan Mountain Region"
        characteristics = "Variable fertility, rich in organic matter in forested areas"
        suitable_crops = ["Tea", "Apples", "Pears", "Stone fruits", "Potato", "Barley", "Buckwheat"]
        
    elif (latitude >= 8.0 and latitude <= 22.0 and longitude >= 72.0 and longitude <= 75.0) or \
         (latitude >= 8.0 and latitude <= 20.0 and longitude >= 80.0 and longitude <= 88.0):
        
        soil_type = "Coastal Alluvial Soil"
        sand, clay, silt = 50, 25, 25
        ph = 7.1
        ph_status = "Neutral"
        texture = "Sandy Loam"
        region = "Coastal Plains"
        characteristics = "Mixed sand & silt, influenced by sea, varies in salinity"
        suitable_crops = ["Coconut", "Rice", "Cashew", "Fruits", "Vegetables", "Coconut"]
        
    elif (latitude >= 24.0 and latitude <= 30.0 and longitude >= 70.0 and longitude <= 75.0):
        
        soil_type = "Desert Scrub Soil"
        sand, clay, silt = 70, 15, 15
        ph = 8.0
        ph_status = "Alkaline"
        texture = "Sandy"
        region = "Desert Transition Zone"
        characteristics = "Semi-arid, low organic matter, improving with irrigation"
        suitable_crops = ["Guar (Cluster Bean)", "Millets", "Mustard", "Pulses", "Cumin"]
        
    else:
        soil_type = "Mixed Loamy Soil"
        sand, clay, silt = 45, 30, 25
        ph = 6.8
        ph_status = "Neutral"
        texture = "Loamy"
        region = "Central Mixed Region"
        characteristics = "Well-balanced soil, moderate fertility"
        suitable_crops = ["Soybean", "Wheat", "Gram (Chickpea)", "Maize", "Vegetables"]
    
    print("\n" + "="*60)
    print("🌱 SOIL IDENTIFICATION REPORT (OFFLINE)")
    print("="*60)
    print(f"\n📍 Location: {latitude}°N, {longitude}°E")
    print(f"🗺️  Region: {region}")
    print(f"\n🏷️  SOIL TYPE: {soil_type}")
    print(f"📋 Texture: {texture}")
    
    print(f"\n📊 SOIL COMPOSITION:")
    print(f"   • Sand: {sand:.1f}%")
    print(f"   • Silt: {silt:.1f}%")
    print(f"   • Clay: {clay:.1f}%")
    print(f"   • pH: {ph:.1f} ({ph_status})")
    
    print(f"\n📝 Characteristics:")
    print(f"   {characteristics}")
    
    print(f"\n🌾 Suitable Crops for this soil:")
    for crop in suitable_crops[:6]:
        print(f"   • {crop}")
    
    return {
        'soil_type': soil_type,
        'sand': sand,
        'silt': silt,
        'clay': clay,
        'ph': ph,
        'ph_status': ph_status,
        'texture': texture,
        'region': region,
        'characteristics': characteristics,
        'suitable_crops': suitable_crops,
        'latitude': latitude,
        'longitude': longitude
    }

print("\n" + "="*60)
print("📍 STEP 3: SELECT COORDINATE SOURCE")
print("="*60)

print("\nChoose option:")
print("1. Use coordinates from satellite image (auto-detected)")
print("2. Enter your own coordinates (AOI)")

choice = input("\nEnter 1 or 2: ")

if choice == "1":
    lat = image_center_lat
    lon = image_center_lon
    soil_data = get_soil_offline(lat, lon)
    
elif choice == "2":
    try:
        lat = float(input("\nEnter Latitude (e.g., 28.6139 for Delhi): "))
        lon = float(input("Enter Longitude (e.g., 77.2090 for Delhi): "))
        soil_data = get_soil_offline(lat, lon)
    except ValueError:
        print("❌ Invalid coordinates. Using image coordinates instead.")
        lat = image_center_lat
        lon = image_center_lon
        soil_data = get_soil_offline(lat, lon)
else:
    print("Invalid choice. Using image coordinates.")
    lat = image_center_lat
    lon = image_center_lon
    soil_data = get_soil_offline(lat, lon)

print("\n" + "="*60)
print("📋 FINAL SUMMARY REPORT")
print("="*60)

print(f"""

  SATELLITE IMAGE ANALYSIS                                  

  💧 Water Area: {water_pct:.1f}%                                            
  🌿 Vegetation Area: {veg_pct:.1f}%                                         
  🏙️  Urban Area: {urban_pct:.1f}%                                           

  SOIL ANALYSIS (OFFLINE)                                   

  📍 Location: {lat:.4f}°, {lon:.4f}°                                         
  🏷️  Soil Type: {soil_data['soil_type'][:35]}│
  📋 Texture: {soil_data['texture']}                                           
  📊 Composition: Sand {soil_data['sand']:.0f}% / Silt {soil_data['silt']:.0f}% / Clay {soil_data['clay']:.0f}%   
  🧪 pH Level: {soil_data['ph']:.1f} ({soil_data['ph_status']})                             
  🗺️  Region: {soil_data['region'][:40]}│

""")

print("\n✅ Analysis Complete!")