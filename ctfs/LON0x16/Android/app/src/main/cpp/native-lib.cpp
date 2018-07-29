#include <string.h>
#include <jni.h>

extern "C" {

// Strings obfuscated by https://zerosum0x0.blogspot.com/2017/08/obfuscatedencrypted-cc-online-string.html

// flag{progressive_conductor_emotion}
JNIEXPORT jstring JNICALL
Java_com_imhotepisinvisible_sectalkslon0x16_MainActivity_stringFromJNI1(JNIEnv *env, jobject thiz) {
    unsigned char s[] =
            {

                    0x32, 0x14, 0x5, 0x3, 0xf6, 0x28, 0x1a, 0x73,
                    0x43, 0x3d, 0x71, 0x66, 0x3e, 0x1c, 0xb6, 0xc,
                    0x89, 0xfb, 0x57, 0xbb, 0x7a, 0xf0, 0x4b, 0x2d,
                    0x2a, 0x1b, 0x95, 0x74, 0xd4, 0x36, 0x15, 0x68,
                    0xfa, 0xdf, 0x64, 0xed
            };

    for (unsigned int m = 0; m < sizeof(s); ++m) {
        unsigned char c = s[m];
        c = (c >> 0x3) | (c << 0x5);
        c = ~c;
        c = (c >> 0x1) | (c << 0x7);
        c ^= 0x85;
        c -= m;
        c = -c;
        c += 0x32;
        c ^= m;
        c += 0xac;
        c = (c >> 0x7) | (c << 0x1);
        c ^= m;
        c = (c >> 0x5) | (c << 0x3);
        c += m;
        c ^= 0x3e;
        c -= m;
        s[m] = c;
    }

    return env->NewStringUTF((char *) s);
}

// http://imhotepisinvisible.com:34567
JNIEXPORT jstring JNICALL
Java_com_imhotepisinvisible_sectalkslon0x16_MainActivity_stringFromJNI2(JNIEnv *env, jobject thiz) {
    unsigned char s[] =
            {

                    0x2f, 0xae, 0xf, 0xcf, 0x42, 0x5b, 0xdb, 0x8a,
                    0x4a, 0xd2, 0x5b, 0xb3, 0x8c, 0x95, 0xec, 0xbd,
                    0xad, 0xe5, 0x25, 0xe, 0xfe, 0x4f, 0xc7, 0x78,
                    0x90, 0xea, 0xc0, 0xe1, 0xd1, 0xcc, 0x45, 0x3d,
                    0x14, 0xad, 0x25, 0x5d
            };

    for (unsigned int m = 0; m < sizeof(s); ++m) {
        unsigned char c = s[m];
        c = -c;
        c += m;
        c = ~c;
        c = -c;
        c -= 0xe0;
        c = (c >> 0x7) | (c << 0x1);
        c = ~c;
        c += m;
        c ^= 0x1f;
        c = -c;
        c = (c >> 0x5) | (c << 0x3);
        c += m;
        c ^= m;
        c = (c >> 0x7) | (c << 0x1);
        c ^= 0xd7;
        s[m] = c;
    }

    return env->NewStringUTF((char *) s);
}

// X-Admin
JNIEXPORT jstring JNICALL
Java_com_imhotepisinvisible_sectalkslon0x16_MainActivity_stringFromJNI3(JNIEnv *env, jobject thiz) {
    unsigned char s[] =
            {

                    0x6a, 0xd4, 0xfe, 0x6f, 0xc6, 0xfc, 0xd8, 0xb2
            };

    for (unsigned int m = 0; m < sizeof(s); ++m) {
        unsigned char c = s[m];
        c -= 0x7a;
        c ^= m;
        c = ~c;
        c = -c;
        c ^= 0x3c;
        c += m;
        c = ~c;
        c ^= m;
        c = ~c;
        c = (c >> 0x5) | (c << 0x3);
        c -= m;
        c ^= m;
        c -= 0x1a;
        c = (c >> 0x7) | (c << 0x1);
        c = -c;
        s[m] = c;
    }

    return env->NewStringUTF((char *) s);
}

// False
JNIEXPORT jstring JNICALL
Java_com_imhotepisinvisible_sectalkslon0x16_MainActivity_stringFromJNI4(JNIEnv *env, jobject thiz) {
    unsigned char s[] =
            {

                    0xed, 0xf3, 0xee, 0xee, 0xa2, 0xb
            };

    for (unsigned int m = 0; m < sizeof(s); ++m) {
        unsigned char c = s[m];
        c += 0x6;
        c ^= m;
        c += m;
        c ^= m;
        c += 0xe6;
        c = ~c;
        c -= m;
        c = -c;
        c = (c >> 0x6) | (c << 0x2);
        c += 0xdb;
        c = -c;
        c -= m;
        c = -c;
        c += m;
        c ^= m;
        s[m] = c;
    }

    return env->NewStringUTF((char *) s);
}

}