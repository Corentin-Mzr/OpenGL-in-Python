#version 330 core

struct PointLight
{
    vec3 position;
    vec3 color;
    float strength;
};

in vec2 fragmentTexCoord;
in vec3 fragmentPosition;
in vec3 fragmentNormal;

uniform sampler2D imageTexture;
uniform PointLight Lights[8];
uniform vec3 cameraPosition;
uniform vec3 tint;

out vec4 color;

vec3 computePointLight(PointLight light, vec3 fragmentPosition, vec3 fragmentNormal);

void main()
{
    // Ambient lighting
    vec4 baseTexture = texture(imageTexture, fragmentTexCoord);
    vec3 temp = 0.2 * baseTexture.rgb;

    for (int i = 0; i < 8; ++i){
        temp += computePointLight(Lights[i], fragmentPosition, fragmentNormal);
    }
    color = vec4(temp, baseTexture.a);
}

vec3 computePointLight(PointLight light, vec3 fragmentPosition, vec3 fragmentNormal)
{
    vec3 result = vec3(0.0);
    vec3 baseTexture = texture(imageTexture, fragmentTexCoord).rgb;

    // Geometric data
    vec3 fragLight = light.position - fragmentPosition;
    float distance = length(fragLight);
    fragLight = normalize(fragLight);
    vec3 fragCamera = normalize(cameraPosition - fragmentPosition);
    vec3 halfVec = normalize(fragLight + fragCamera);

    // Diffusion
    result += light.color * light.strength * max(0.0, dot(fragmentNormal, fragLight)) / (distance * distance) * baseTexture;

    // Specular
    result += light.color * light.strength * pow(max(0.0, dot(fragmentNormal, halfVec)), 32) / (distance * distance);

    return result;
}