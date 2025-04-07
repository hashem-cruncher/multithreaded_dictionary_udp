# Multithreaded Dictionary Server - خادم القاموس متعدد المسارات

A client-server application that implements a multithreaded dictionary server with a graphical client.

تطبيق قائم على هيكلية العميل-خادم ينفذ خادم قاموس متعدد المسارات مع واجهة رسومية للعميل.

## Project Features - ميزات المشروع

- **Multithreaded Server**: Implements worker pool architecture
- **UDP Communication**: Reliable communication through request-response pattern and retry mechanisms
- **Dictionary Lookup**: Fast in-memory word lookup with full JSON dictionary
- **Graphical Client**: PyQt5-based UI for easy dictionary lookups

- **خادم متعدد المسارات**: ينفذ هيكلية تجمع العمال
- **اتصال UDP**: اتصال موثوق من خلال نمط الطلب-استجابة وآليات إعادة المحاولة
- **بحث القاموس**: بحث سريع في الذاكرة عن الكلمات مع قاموس JSON كامل
- **واجهة رسومية للعميل**: واجهة مستخدم تعتمد على PyQt5 لعمليات بحث سهلة في القاموس

## Architecture - الهيكل المعماري

### Server Components - مكونات الخادم
- UDP socket for receiving requests
- Thread pool for handling multiple client requests concurrently
- JSON dictionary manager for efficient word lookups
- Request-response protocol using JSON format

- مقبس UDP لاستقبال الطلبات
- تجمع المسارات لمعالجة طلبات العملاء المتعددة بشكل متزامن
- مدير قاموس JSON للبحث الفعال عن الكلمات
- بروتوكول الطلب-استجابة باستخدام تنسيق JSON

### Client Components - مكونات العميل
- Graphical User Interface (PyQt5)
- Asynchronous request handling
- Client-side retry mechanism for network errors
- Result caching for performance

- واجهة المستخدم الرسومية (PyQt5)
- معالجة الطلبات بشكل غير متزامن
- آلية إعادة المحاولة من جانب العميل لأخطاء الشبكة
- تخزين مؤقت للنتائج لتحسين الأداء

## Requirements - المتطلبات

- Python 3.6+
- PyQt5 (for the client GUI)

- بايثون 3.6 أو أعلى
- PyQt5 (لواجهة المستخدم الرسومية للعميل)

## Running the Application - تشغيل التطبيق

### Starting the Server - تشغيل الخادم

```bash
python -m server.udp_server <port> <dictionary-file>
```

Example - مثال:
```bash
python -m server.udp_server 12345 data/dictionary.json
```

### Starting the Client - تشغيل العميل

```bash
python -m client.udp_client_gui <server-address> <server-port>
```

Example - مثال:
```bash
python -m client.udp_client_gui localhost 12345
```

## Project Structure - هيكل المشروع

- `server/`: Server-side code - كود جانب الخادم
  - `udp_server.py`: Main server implementation - التنفيذ الرئيسي للخادم
  - `request_handler.py`: Worker pool and request processing - تجمع العمال ومعالجة الطلبات
  - `json_dictionary.py`: Dictionary management - إدارة القاموس
- `client/`: Client-side code - كود جانب العميل
  - `udp_client_gui.py`: GUI implementation - تنفيذ الواجهة الرسومية
  - `udp_client_comm.py`: Communication with server - الاتصال مع الخادم
- `data/`: Data files - ملفات البيانات
  - `dictionary.json`: Dictionary data in JSON format - بيانات القاموس بتنسيق JSON

## Communication Protocol - بروتوكول الاتصال

The client and server communicate using JSON-formatted messages. Each message contains an action, timestamp, and other action-specific fields.

يتواصل العميل والخادم باستخدام رسائل بتنسيق JSON. تحتوي كل رسالة على إجراء، وطابع زمني، وحقول أخرى خاصة بالإجراء.

### Sample Request (Lookup) - نموذج طلب (بحث)
```json
{
  "action": "lookup",
  "word": "algorithm",
  "timestamp": 1649425678.123,
  "id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Sample Response (Word Found) - نموذج استجابة (تم العثور على الكلمة)
```json
{
  "status": "found",
  "word": "algorithm",
  "definition": "A step-by-step procedure or formula for solving a problem...",
  "timestamp": 1649425678.456
}
```

## Error Handling - معالجة الأخطاء

The application implements comprehensive error handling:
- Network communication errors (timeouts, connection issues)
- Input validation
- Dictionary file errors
- Server-side exceptions
- Client-side retry mechanisms

يقوم التطبيق بتنفيذ معالجة شاملة للأخطاء:
- أخطاء اتصال الشبكة (انتهاء مهلة الاتصال، مشاكل الاتصال)
- التحقق من صحة المدخلات
- أخطاء ملف القاموس
- استثناءات جانب الخادم
- آليات إعادة المحاولة من جانب العميل

## Implementation Details - تفاصيل التنفيذ

- **Thread Pool**: Implements a configurable number of worker threads
- **Timeout Handling**: Socket timeouts with client retries
- **Unique Request IDs**: For tracking request-response pairs
- **Logging**: Comprehensive logging throughout the application

- **تجمع المسارات**: ينفذ عددًا قابلاً للتكوين من مسارات العمال
- **معالجة انتهاء المهلة**: انتهاء مهلة المقبس مع إعادة محاولات العميل
- **معرفات الطلب الفريدة**: لتتبع أزواج الطلب-استجابة
- **التسجيل**: تسجيل شامل عبر التطبيق

