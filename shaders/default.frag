#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;
in vec4 shadowCoord;

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform Light light;
uniform sampler2D u_texture_0;
uniform vec3 camPos;
uniform sampler2DShadow shadowMap;
uniform vec2 u_resolution;
uniform bool menuOpen;

float lookup(float ox, float oy) {
    vec2 pixelOffset = 1 / u_resolution;
    return textureProj(shadowMap, shadowCoord + vec4(ox * pixelOffset.x * shadowCoord.w, oy * pixelOffset.y * shadowCoord.w, 0.0, 0.0));
}

// This technique is called Percentage-Closer Filtering (PCF)
// https://developer.nvidia.com/gpugems/gpugems/part-ii-lighting-and-shadows/chapter-11-shadow-map-antialiasing
float getSoftShadowX16() {
    float shadow = 0;
    float swidth = 1.0;
    float endp = swidth * 1.5;
    for (float y = -endp; y <= endp; y += swidth) {
        for (float x = -endp; x <= endp; x += swidth) {
            shadow += lookup(x, y);
        }
    }
    return shadow / 16.0;
}

float getShadow() {
    float shadow = textureProj(shadowMap, shadowCoord);
    return shadow;
}

vec3 getLight(vec3 color) {
    vec3 Normal = normalize(normal);
    
    // Ambient Light
    vec3 ambient = light.Ia;
    
    // Diffuse Light
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    vec3 diffuse = diff * light.Id;

    // Specular
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 128);
    vec3 specular = spec * light.Is;

    // Shadow 
    float shadow = getSoftShadowX16();

    return color * (ambient + (diffuse + specular) * shadow);
}

void main() {
    if(menuOpen) {
        vec2 fragCoord = gl_FragCoord.xy;
        float screenWidth = 1600.0;
        float leftBoundary = 0.2 * screenWidth;
        if (fragCoord.x < leftBoundary) {
            discard;
        }
    }

    // https://learnopengl.com/Advanced-Lighting/Gamma-Correction
    float gamma = 2.2;
    
    vec3 color = texture(u_texture_0, uv_0).rgb;
    color = pow(color, vec3(gamma));
    color = getLight(color);
    color = pow(color, 1 / vec3(gamma));
    fragColor = vec4(color, 1.0); 

    // fragColor = mix(fragColor, vec4(1.), 0.5);
}