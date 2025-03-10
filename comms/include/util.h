/**
 * [util.h] Provides numeric type definitions and common
 * math functions.
 */
#pragma once

#include <Arduino.h>
#include <stdint.h>
#include <stddef.h>

#define len(x) (sizeof((x)) / sizeof((x)[0]))
#define simple_task(n, f) xTaskCreate([](void *_args) f, (n), 2048, NULL, 1, NULL)
#define stringify_indirection(x) #x
#define stringify(x) stringify_indirection(x)

typedef size_t usize;
// 8-bit
typedef uint8_t u8;
typedef int8_t i8;
// 16-bit
typedef uint16_t u16;
typedef int16_t i16;
// 32-bit
typedef uint32_t u32;
typedef int32_t i32;
// 64-bit
typedef uint64_t u64;
typedef int64_t i64;
// Floating-point
typedef float f32;
typedef double f64;

static void panic(const char *msg) {
    while (true) {
        Serial.println(msg);
        delay(100);
    }
}